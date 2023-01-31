from cvlac import db_gruplac
import pandas
from cvlac.gruplac_models.OtrosTecnologicos import OtrosTecnologicos

class OtrosTecnologicosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_gruplac.session.bulk_insert_mappings(OtrosTecnologicos, dicList)
        try:
            db_gruplac.session.commit()
        except:
            db_gruplac.session.rollback()
            print("No se pudo insertar el dataframe en OtrosTecnologicos")
            df.to_csv('OtrosTecnologicosGruplac.csv')
        finally:
            db_gruplac.session.close()
    
    def delete_idgruplac(self, idgruplac):
        db_gruplac.session.query(OtrosTecnologicos).filter(OtrosTecnologicos.idgruplac==idgruplac).delete(synchronize_session=False)
        try:
            db_gruplac.session.commit()
        except:
            db_gruplac.session.rollback()
            print("No se pudo eliminar el idgruplac: "+idgruplac+" en OtrosTecnologicos")
        finally:
            db_gruplac.session.close()