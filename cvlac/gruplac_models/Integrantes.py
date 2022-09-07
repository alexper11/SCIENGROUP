from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class Integrantes(Base):
    
    __tablename__ = 'integrantes'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    url = Column(String(400), nullable=True)
    integrante = Column(String(400), nullable=True)
    vinculacion = Column(String(50), nullable=False)
    horas = Column(Integer(5), nullable=True)
    fecha_vinculacion = Column(String(150), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Integrantes({self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac