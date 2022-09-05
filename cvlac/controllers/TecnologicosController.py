from cvlac import db_cvlac
import pandas
from cvlac.models.Tecnologicos import Tecnologicos

class TecnologicosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            tecnologicos = Tecnologicos(**dic)
            db_cvlac.session.add(tecnologicos)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Tecnologicos")
            df.to_csv('TecnologicosCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()