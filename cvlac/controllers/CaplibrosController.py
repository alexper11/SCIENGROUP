from cvlac import db_cvlac
import pandas
from cvlac.models.Caplibros import Caplibros

class CaplibrosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            caplibros = Caplibros(**dic)
            db_cvlac.session.add(caplibros)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Caplibros")
            df.to_csv('CaplibrosCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    