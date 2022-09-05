from cvlac import db
import pandas
from cvlac.cvlac_models.Investigacion import Investigacion

class InvestigacionController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            investigacion = Investigacion(**dic)
            db.session.add(investigacion)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Investigacion")
            df.to_csv('InvestigacionCvlac.csv')
            raise
        finally:
            db.session.close()
    