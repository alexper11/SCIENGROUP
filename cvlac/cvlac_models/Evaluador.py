from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Evaluador(Base):
    
    __tablename__ = 'evaluador'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    ambito = Column(String(300), nullable=True)
    par_evaluador = Column(String(200), nullable=True)
    editorial = Column(String(500), nullable=True)
    revista = Column(String(500), nullable=True)
    institucion = Column(String(500), nullable=True)
    fecha = Column(String(100), nullable=True)
    
    basico = relationship('Basico', backref='evaluador')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Evaluador({self.ambito}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac