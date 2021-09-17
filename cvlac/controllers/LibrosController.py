from cvlac import db
import pandas
from cvlac.models.Libros import Libros

class LibrosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            libros = Libros(**dic)
            db.session.add(libros)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Libros")
            df.to_csv('LibrosCvlac.csv')
            raise
        finally:
            db.session.close()
    