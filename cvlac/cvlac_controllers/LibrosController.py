from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Libros import Libros

class LibrosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            libros = Libros(**dic)
            db_cvlac.session.add(libros)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Libros")
            df.to_csv('LibrosCvlac.csv')
            raise
        finally:
            db_cvlac.session.close()
    