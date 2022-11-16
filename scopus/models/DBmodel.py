from scopus.scopusdb import Base, engine
from sqlalchemy_utils import database_exists, create_database

from scopus.models.Autores import Autores
from scopus.models.Productos import Productos
from scopus.models.MetaDBSco import MetaDBSco


def create_scopus_db():
    
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)