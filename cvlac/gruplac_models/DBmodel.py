
from cvlac.db_gruplac import Base, engine
from sqlalchemy_utils import database_exists, create_database

from cvlac.gruplac_models.Basico import Basico
from cvlac.gruplac_models.CursoDoctorado import CursoDoctorado
from cvlac.gruplac_models.CursoMaestria import CursoMaestria
from cvlac.gruplac_models.Instituciones import Instituciones
from cvlac.gruplac_models.Integrantes import Integrantes
from cvlac.gruplac_models.Lineas import Lineas
from cvlac.gruplac_models.OtroPrograma import OtroPrograma
from cvlac.gruplac_models.ProgramaDoctorado import ProgramaDoctorado
from cvlac.gruplac_models.ProgramaMaestria import ProgramaMaestria
from cvlac.gruplac_models.MetaDB import MetaDB

def create_gruplac_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)