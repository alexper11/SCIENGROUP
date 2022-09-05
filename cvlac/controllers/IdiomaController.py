from cvlac import db
import pandas
from cvlac.cvlac_models.Idioma import Idioma

class IdiomaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            idioma = Idioma(**dic)
            db.session.add(idioma)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Idioma")
            df.to_csv('IdiomaCvlac.csv')
            raise
        finally:
            db.session.close()
    