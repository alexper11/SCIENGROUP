from typing import Tuple
from scopus.scopusdb import Base
from sqlalchemy import Column, Integer, String

class ArticulosSco(Base):
    
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    scopus_id = Column(String(50), nullable=False)
    eid = Column(String(50), nullable=True)
    titulo = Column(String(600), nullable=False)
    creador = Column(String(150), nullable=False)
    nombre_publicacion= Column(String(200), nullable=True)
    eissn = Column(String(50), nullable=True)
    issn = Column(String(50), nullable=True)
    volumen = Column(String(20), nullable=True)
    paginas = Column(String(20), nullable=True)
    fecha_publicacion = Column(String(20), nullable=True)
    doi = Column(String(250), nullable=True)
    citado = Column(String(20), nullable=True)
    afiliacion = Column(String(1500), nullable=True)
    tipo_fuente = Column(String(100), nullable=True)
    tipo_documento = Column(String(100), nullable=True)
    autores = Column(String(5000), nullable=True)
    autores_id = Column(String(3000), nullable=True)
    palabras_clave = Column(String(800), nullable=True)
    agencia_fundadora = Column(String(300), nullable=True)
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'ArticulosSco({self.nombre}, {self.autor_id})'
    
    def __str__(self):
        return self.autor_id