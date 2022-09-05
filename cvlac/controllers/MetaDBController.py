from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.MetaDB import MetaDB

class MetaDBController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_datetime(self):
        metadb=MetaDB()
        db_cvlac.session.add(metadb)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar datetime en MetDB")
            raise
        finally:
            db_cvlac.session.close()
    