from cvlac import db
import pandas
from cvlac.models.Software import Software

class SoftwareController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            software = Software(**dic)
            db.session.add(software)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en Software")
            df.to_csv('SoftwareCvlac.csv')
            raise
        finally:
            db.session.close()
    