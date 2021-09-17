from cvlac import db
import pandas
from cvlac.models.Redes import Redes

class RedesController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            redes = Redes(**dic)
            db.session.add(redes)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Redes")
            df.to_csv('RedesCvlac.csv')
            raise
        finally:
            db.session.close()
    