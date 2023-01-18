from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Estancias import Estancias

class EstanciasController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_cvlac.session.bulk_insert_mappings(Estancias, dicList)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Estancias")
            df.to_csv('EstanciasCvlac.csv')
        finally:
            db_cvlac.session.close()
            
    def delete_idcvlac(self, idcvlac):
        db_cvlac.session.query(Estancias).filter(Estancias.idcvlac==idcvlac).delete(synchronize_session=False)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo eliminar el idcvlac: "+idcvlac+" en Estancias")
        finally:
            db_cvlac.session.close()