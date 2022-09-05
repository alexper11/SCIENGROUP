from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Actuacion import Actuacion

class ActuacionController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            actuacion = Actuacion(**dic)
            db_cvlac.session.add(actuacion)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Actuacion")
            df.to_csv('ActuacionCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    
    
            
    
    