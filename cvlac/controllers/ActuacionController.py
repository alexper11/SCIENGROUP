from cvlac import db
import pandas
from cvlac.models.Actuacion import Actuacion

class ActuacionController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            actuacion = Actuacion(**dic)
            db.session.add(actuacion)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Actuacion")
            df.to_csv('ActuacionCvlac.csv')
            raise
        finally:
            db.session.close()
    
    
            
    
    