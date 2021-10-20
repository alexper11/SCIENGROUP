from scopus import scopusdb
import pandas
from scopus.models.MetaDBSco import MetaDBSco

class MetaDBScoController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_datetime(self):
        metadb=MetaDBSco()
        scopusdb.session.add(metadb)
        try:
            scopusdb.session.commit()
        except:
            scopusdb.session.rollback()
            print("No se pudo insertar datetime en MetDB")
            raise
        finally:
            scopusdb.session.close()
    