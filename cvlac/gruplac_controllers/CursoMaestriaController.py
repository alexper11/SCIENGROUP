from cvlac import db_gruplac
import pandas
from cvlac.gruplac_models.CursoMaestria import CursoMaestria

class CursoMaestriaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            curso_maestria = CursoMaestria(**dic)
            db_gruplac.session.add(curso_maestria)
        try:
            db_gruplac.session.commit()
        except:
            db_gruplac.session.rollback()
            print("No se pudo insertar el dataframe en CursoMaestria")
            df.to_csv('CursoMaestriaGruplac.csv')
            raise
        finally:
            db_gruplac.session.close()
    