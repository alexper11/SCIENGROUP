from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String

class Evaluador(Base):
    
    __tablename__ = 'evaluador'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    ambito = Column(String(300), nullable=False)
    par_evaluador = Column(String(200), nullable=False)
    editorial = Column(String(500), nullable=True)
    revista = Column(String(500), nullable=True)
    institucion = Column(String(500), nullable=True)
    fecha = Column(String(60), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Evaluador({self.ambito}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac