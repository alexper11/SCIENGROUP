
from cvlac.db_cvlac import Base, engine
from sqlalchemy_utils import database_exists, create_database

from cvlac.cvlac_models.Articulos import Articulos
from cvlac.cvlac_models.Actuacion import Actuacion
from cvlac.cvlac_models.Basico import Basico
from cvlac.cvlac_models.Evaluador import Evaluador
from cvlac.cvlac_models.Identificadores import Identificadores
from cvlac.cvlac_models.Idioma import Idioma
from cvlac.cvlac_models.Investigacion import Investigacion
from cvlac.cvlac_models.Jurados import Jurados
from cvlac.cvlac_models.Reconocimiento import Reconocimiento
from cvlac.cvlac_models.Redes import Redes
from cvlac.cvlac_models.Libros import Libros
from cvlac.cvlac_models.Estancias import Estancias
from cvlac.cvlac_models.Academica import Academica
from cvlac.cvlac_models.Complementaria import Complementaria
from cvlac.cvlac_models.Caplibros import Caplibros
from cvlac.cvlac_models.Software import Software
from cvlac.cvlac_models.Prototipo import Prototipo
from cvlac.cvlac_models.MetaDB import MetaDB

def create_cvlac_db():
    
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)