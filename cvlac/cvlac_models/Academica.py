from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Academica(Base):
    
    __tablename__ = 'academica'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    tipo = Column(String(150), nullable=True)
    institucion = Column(String(600), nullable=True)
    titulo = Column(String(600), nullable=True)
    fecha = Column(String(200), nullable=True)
    proyecto = Column(String(1000), nullable=True)
    
    basico = relationship('Basico', backref='academica')
    
    def __init__(self, **kwargs):  
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Academica({self.tipo}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac