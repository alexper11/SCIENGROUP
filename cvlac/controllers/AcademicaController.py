from cvlac import db
import pandas
from cvlac.cvlac_models.Academica import Academica

class AcademicaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            academica = Academica(**dic)
            db.session.add(academica)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Academica")
            df.to_csv('AcademicaCvlac.csv')
            raise
        finally:
            db.session.close()