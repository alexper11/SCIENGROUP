from cvlac import db_cvlac
import pandas
from cvlac.models.Reconocimiento import Reconocimiento

class ReconocimientoController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            reconocimiento = Reconocimiento(**dic)
            db_cvlac.session.add(reconocimiento)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Reconocimiento")
            df.to_csv('ReconocimientoCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    