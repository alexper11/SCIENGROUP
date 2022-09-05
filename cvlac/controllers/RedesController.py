from cvlac import db_cvlac
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
            db_cvlac.session.add(redes)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Redes")
            df.to_csv('RedesCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    