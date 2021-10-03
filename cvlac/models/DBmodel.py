
from cvlac.db import Base, engine

from cvlac.models.Articulos import Articulos
from cvlac.models.Actuacion import Actuacion
from cvlac.models.Basico import Basico
from cvlac.models.Evaluador import Evaluador
from cvlac.models.Identificadores import Identificadores
from cvlac.models.Idioma import Idioma
from cvlac.models.Investigacion import Investigacion
from cvlac.models.Jurados import Jurados
from cvlac.models.Reconocimiento import Reconocimiento
from cvlac.models.Redes import Redes
from cvlac.models.Libros import Libros
from cvlac.models.Estancias import Estancias
from cvlac.models.Academica import Academica
from cvlac.models.Complementaria import Complementaria
from cvlac.models.MetaDB import MetaDB

def create_db():
    #######################
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    ###########################