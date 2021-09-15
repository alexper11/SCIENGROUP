from cvlac import db
import pandas
from cvlac.models.Complementaria import Complementaria

class ComplementariaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            complementaria = Complementaria(**dic)
            db.session.add(complementaria)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Complementaria")
        finally:
            db.session.close()