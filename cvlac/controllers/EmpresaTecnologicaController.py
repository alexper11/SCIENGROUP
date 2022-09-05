from cvlac import db_cvlac
import pandas
from cvlac.models.EmpresaTecnologica import EmpresaTecnologica

class EmpresaTecnologicaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            empresatecnologica = EmpresaTecnologica(**dic)
            db_cvlac.session.add(empresatecnologica)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en EmpresaTecnologica")
            df.to_csv('EmpresaTecnologicaCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    