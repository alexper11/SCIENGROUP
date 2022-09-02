from cvlac import db
import pandas
from cvlac.models.Prototipo import Prototipo

class PrototipoController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            prototipo = Prototipo(**dic)
            db.session.add(prototipo)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Prototipo")
            df.to_csv('PrototipoCvlac.csv')
            raise
        finally:
            db.session.close()