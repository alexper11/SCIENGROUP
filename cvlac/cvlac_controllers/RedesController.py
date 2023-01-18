from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Redes import Redes

class RedesController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_cvlac.session.bulk_insert_mappings(Redes, dicList)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Redes")
            df.to_csv('RedesCvlac.csv')
        finally:
            db_cvlac.session.close()
    
    def delete_idcvlac(self, idcvlac):
        db_cvlac.session.query(Redes).filter(Redes.idcvlac==idcvlac).delete(synchronize_session=False)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo eliminar el idcvlac: "+idcvlac+" en Redes")
        finally:
            db_cvlac.session.close()