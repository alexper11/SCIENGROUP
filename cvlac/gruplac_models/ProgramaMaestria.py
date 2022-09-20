from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class ProgramaMaestria(Base):
    
    __tablename__ = 'programa_maestria'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    programa = Column(String(500), nullable=True)
    fecha = Column(String(60), nullable=True)
    acto = Column(String(300), nullable=True)
    institucion = Column(String(600), nullable=True)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'ProgramaMaestria({self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac