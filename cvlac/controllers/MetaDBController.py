from cvlac import db
import pandas
from cvlac.cvlac_models.MetaDB import MetaDB

class MetaDBController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_datetime(self):
        metadb=MetaDB()
        db.session.add(metadb)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar datetime en MetDB")
            raise
        finally:
            db.session.close()
    