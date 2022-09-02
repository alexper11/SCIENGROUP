from cvlac import db
import pandas
from cvlac.models.InnovacionEmpresarial import InnovacionEmpresarial

class InnovacionEmpresarialController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            innovacion_empresarial = InnovacionEmpresarial(**dic)
            db.session.add(innovacion_empresarial)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print("No se pudo insertar el dataframe en InnovacionEmpresarial")
            df.to_csv('InnovacionEmpresarialCvlac.csv')
            raise
        finally:
            db.session.close()