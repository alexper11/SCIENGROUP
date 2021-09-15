from scopus.models.Autores import Autores
from scopus import scopusdb
import pandas
from scopus.models.Autores import Autores

class AutoresController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            autores = Autores(**dic)
            scopusdb.session.add(autores)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo insertar el dataframe en Autores")
        finally:
            scopusdb.session.close()