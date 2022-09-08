from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class CursoMaestria(Base):
    
    __tablename__ = 'curso_maestria'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    curso = Column(String(400), nullable=True)
    fecha = Column(String(60), nullable=True)
    acto = Column(String(50), nullable=True)
    programa = Column(String(200), nullable=True)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'CursoMaestria({self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac