from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Idioma import Idioma

class IdiomaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_cvlac.session.bulk_insert_mappings(Idioma, dicList)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Idioma")
            df.to_csv('IdiomaCvlac.csv')
        finally:
            db_cvlac.session.close()
    
    def delete_idcvlac(self, idcvlac):
        db_cvlac.session.query(Idioma).filter(Idioma.idcvlac==idcvlac).delete(synchronize_session=False)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo eliminar el idcvlac: "+idcvlac+" en Idioma")
        finally:
            db_cvlac.session.close()