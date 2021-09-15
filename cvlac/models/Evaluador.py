from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Evaluador(Base):
    
    __tablename__ = 'evaluador'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    ambito = Column(String(40), nullable=False)
    par_evaluador = Column(String(50), nullable=False)
    editorial = Column(String(200), nullable=True)
    revista = Column(String(200), nullable=True)
    institucion = Column(String(250), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Evaluador({self.ambito}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac