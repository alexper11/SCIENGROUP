from cvlac import db_gruplac
import pandas
from cvlac.gruplac_models.MetaDB import MetaDB

class MetaGruplacDBController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_datetime(self):
        metadb=MetaDB()
        db_gruplac.session.add(metadb)
        try:
            db_gruplac.session.commit()
        except:
            db_gruplac.session.rollback()
            print("No se pudo insertar datetime en MetaDB gruplac")
            raise
        finally:
            db_gruplac.session.close()
    