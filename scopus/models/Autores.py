from scopus.scopusdb import Base
from sqlalchemy import Column, Integer, String

class Autores(Base):
    
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(300), nullable=False)
    autor_id = Column(String(30), nullable=False)
    eid = Column(String(40), nullable=True)
    orcid = Column(String(40), nullable=True)
    documentos= Column(String(10), nullable=True)
    fecha_creacion = Column(String(20), nullable=True)
    citado = Column(String(10), nullable=True)
    citaciones = Column(String(10), nullable=True)
    h_index = Column(String(10), nullable=True)
    co_autores = Column(String(10), nullable=True)
    estado = Column(String(30), nullable=True)
    areas = Column(String(3000), nullable=True)
    rango_publicacion = Column(String(30), nullable=True)
    institucion = Column(String(300), nullable=True)
    departamento = Column(String(300), nullable=True)
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Autores({self.nombre}, {self.autor_id})'
    
    def __str__(self):
        return self.autor_id