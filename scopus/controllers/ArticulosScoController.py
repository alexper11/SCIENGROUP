from scopus.models.ArticulosSco import ArticulosSco
from scopus import scopusdb
import pandas
from scopus.models.ArticulosSco import ArticulosSco

class ArticulosScoController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            articulosSco = ArticulosSco(**dic)
            scopusdb.session.add(articulosSco)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo insertar el dataframe en ArticulosSco")
            df.to_csv('ArticulosScopus.csv')
            raise
        finally:
            scopusdb.session.close()