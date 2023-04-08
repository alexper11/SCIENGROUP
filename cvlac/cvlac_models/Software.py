from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Software(Base):
    
    __tablename__ = 'software'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    autor = Column(String(4000), nullable=True)
    nombre = Column(String(1000), nullable=True)
    tipo = Column(String(500), nullable=True)
    verificado = Column(Boolean,unique=False, default=True)
    nombre_comercial = Column(String(1000), nullable=True)
    contrato_registro = Column(String(500), nullable=True)
    lugar = Column(String(150), nullable=True)
    fecha = Column(String(500), nullable=True)
    plataforma = Column(String(2000), nullable=True)
    ambiente = Column(String(1000), nullable=True)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    basico = relationship('Basico', backref='software')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Software({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac