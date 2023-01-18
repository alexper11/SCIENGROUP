from scopus.models.Productos import Productos
from scopus import scopusdb
import pandas
from scopus.models.Productos import Productos

class ProductosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        scopusdb.session.bulk_insert_mappings(Productos, dicList)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo insertar el dataframe en Productos")
            df.to_csv('ProductosScopus.csv')
        finally:
            scopusdb.session.close()
            
    def delete_affil_id(self, affid):
        scopusdb.session.query(Productos).filter(Productos.affil_id.like(f'%{affid}%')).delete(synchronize_session=False)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo eliminar el affid: "+affid+" en Productos")
        finally:
            scopusdb.session.close()
            
    def delete_eid(self, eid):
        scopusdb.session.query(Productos).filter(Productos.eid.like(f'%{eid}%')).delete(synchronize_session=False)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo eliminar el eid: "+eid+" en Productos")
        finally:
            scopusdb.session.close()