from scopus.models.Autores import Autores
from scopus import scopusdb
import pandas
from scopus.models.Autores import Autores

class AutoresController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
            
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        scopusdb.session.bulk_insert_mappings(Autores, dicList)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo insertar el dataframe en Autores")
            df.to_csv('AutoresScopus.csv')
        finally:
            scopusdb.session.close()
            
    def delete_affil_id(self, affid):
        scopusdb.session.query(Autores).filter(Autores.affil_id.like(f'%{affid}%')).delete(synchronize_session=False)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo eliminar el affid: "+affid+" en Autores")
        finally:
            scopusdb.session.close()
            
    def delete_autor_id(self, auid):
        scopusdb.session.query(Autores).filter(Autores.autor_id.like(f'%{auid}%')).delete(synchronize_session=False)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo eliminar el autor id: "+auid+" en Autores")
        finally:
            scopusdb.session.close()
            
    """
    record_obj = scopusdb.session.query(Autores).filter(Autores.affil_id.like(f'%{affid}%')).all()
    scopusdb.session.delete(record_obj)
    scopusdb.session.commit()
    """