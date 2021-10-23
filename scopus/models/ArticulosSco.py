from typing import Tuple
from scopus.scopusdb import Base
from sqlalchemy import Column, Integer, String

class ArticulosSco(Base):
    
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    scopus_id = Column(String(100), nullable=False)
    eid = Column(String(200), nullable=True)
    titulo = Column(String(1000), nullable=False)
    creador = Column(String(600), nullable=False)
    nombre_publicacion= Column(String(1500), nullable=True)
    editorial= Column(String(1000), nullable=True)
    issn = Column(String(100), nullable=True)
    isbn = Column(String(100), nullable=True)
    volumen = Column(String(50), nullable=True)
    issue = Column(String(50), nullable=True)
    numero_articulo = Column(String(50), nullable=True)
    pag_inicio = Column(String(50), nullable=True)
    pag_fin = Column(String(50), nullable=True)
    pag_count = Column(String(50), nullable=True)
    fecha_publicacion = Column(String(100), nullable=True)
    idioma = Column(String(200), nullable=True)
    doi = Column(String(1000), nullable=True)
    citado = Column(String(50), nullable=True)
    link = Column(String(2000), nullable=True)
    institucion = Column(String(6000), nullable=True)
    abstract = Column(String(5000), nullable=True)
    tema = Column(String(4000), nullable=True)
    tipo_fuente = Column(String(200), nullable=True)
    tipo_documento = Column(String(200), nullable=True)
    etapa_publicacion = Column(String(50), nullable=True)
    autores = Column(String(6000), nullable=True)
    autores_id = Column(String(6000), nullable=True)
    tipo_acceso =Column(String(200), nullable=True)
    palabras_clave_autor = Column(String(5000), nullable=True)
    palabras_clave_index = Column(String(5000), nullable=True)
    institucion = Column(String(5000), nullable=True)
    agencia_fundadora = Column(String(2000), nullable=True)
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'ArticulosSco({self.nombre}, {self.autor_id})'
    
    def __str__(self):
        return self.autor_id