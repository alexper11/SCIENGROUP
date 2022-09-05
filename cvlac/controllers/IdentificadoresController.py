from cvlac import db
import pandas
from cvlac.cvlac_models.Identificadores import Identificadores

class IdentificadoresController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            identificadores = Identificadores(**dic)
            db.session.add(identificadores)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Identificadores")
            df.to_csv('IdentificadoresCvlac.csv')
            raise
        finally:
            db.session.close()
    