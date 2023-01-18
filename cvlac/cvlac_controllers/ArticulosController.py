from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.Articulos import Articulos

class ArticulosController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_cvlac.session.bulk_insert_mappings(Articulos, dicList)
        """
        for dic in dicList:
            articulos = Articulos(**dic)
            db_cvlac.session.add(articulos)
        """
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en Articulos")
            df.to_csv('ArticulosCvlac.csv')
        finally:
            db_cvlac.session.close()
            
    def delete_idcvlac(self, idcvlac):
        db_cvlac.session.query(Articulos).filter(Articulos.idcvlac==idcvlac).delete(synchronize_session=False)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo eliminar el idcvlac: "+idcvlac+" en Articulos")
        finally:
            db_cvlac.session.close()