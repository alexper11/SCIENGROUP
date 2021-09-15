from scopus.scopusdb import Base, engine

from scopus.models.Autores import Autores


def create_scopus_db():
    #######################
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    ###########################