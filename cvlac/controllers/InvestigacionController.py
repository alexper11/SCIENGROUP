from cvlac import db
import pandas
from cvlac.models.Investigacion import Investigacion

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
        finally:
            db.session.close()
    