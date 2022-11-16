from scopus.models.Productos import Productos
from scopus import scopusdb
import pandas
from scopus.models.Productos import Productos

class ProductosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        scopusdb.session.bulk_insert_mappings(Productos, dicList)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo insertar el dataframe en Productos")
            df.to_csv('ProductosScopus.csv')
        finally:
            scopusdb.session.close()
            
    #pendiente metodo delete