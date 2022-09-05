from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Estancias import Estancias

class EstanciasController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            estancias = Estancias(**dic)
            db_cvlac.session.add(estancias)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Estancias")
            df.to_csv('EstanciasCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()