from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class InnovacionEmpresarial(Base):
    
    __tablename__ = 'innovacion_empresarial'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    autor = Column(String(4000), nullable=True)
    nombre = Column(String(1000), nullable=True)
    tipo = Column(String(500), nullable=True)
    verificado = Column(Boolean,unique=False, default=True)
    nombre_comercial = Column(String(1000), nullable=True)
    contrato_registro = Column(String(300), nullable=True)
    lugar = Column(String(200), nullable=True)
    fecha = Column(String(500), nullable=True)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    basico = relationship('Basico', backref='innovacion_empresarial')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'InnovacionEmpresarial({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac