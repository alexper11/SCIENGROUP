from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Evaluador import Evaluador

class EvaluadorController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            evaluador = Evaluador(**dic)
            db_cvlac.session.add(evaluador)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Evaluador")
            df.to_csv('EvaluadorCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    