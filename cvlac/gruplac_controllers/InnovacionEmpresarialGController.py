from cvlac import db_gruplac
import pandas
from cvlac.gruplac_models.InnovacionEmpresarial import InnovacionEmpresarial

class InnovacionEmpresarialGController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_gruplac.session.bulk_insert_mappings(InnovacionEmpresarial, dicList)
        try:
            db_gruplac.session.commit()
        except:
            db_gruplac.session.rollback()
            print("No se pudo insertar el dataframe en InnovacionEmpresarial")
            df.to_csv('InnovacionEmpresarialGruplac.csv')
        finally:
            db_gruplac.session.close()
    
    def delete_idgruplac(self, idgruplac):
        db_gruplac.session.query(InnovacionEmpresarial).filter(InnovacionEmpresarial.idgruplac==idgruplac).delete(synchronize_session=False)
        try:
            db_gruplac.session.commit()
        except:
            db_gruplac.session.rollback()
            print("No se pudo eliminar el idgruplac: "+idgruplac+" en InnovacionEmpresarial")
        finally:
            db_gruplac.session.close()