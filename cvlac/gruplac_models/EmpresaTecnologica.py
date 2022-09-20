from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, Boolean

class EmpresaTecnologica(Base):
    
    __tablename__ = 'empresa_tecnologica'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    verificado = Column(Boolean,unique=False, default=True)
    tipo = Column(String(200), nullable=True)
    nombre = Column(String(1500), nullable=True)
    fecha = Column(String(100), nullable=True)
    nit = Column(String(300), nullable=True)
    fecha_registro = Column(String(100), nullable=True)
    mercado = Column(String(300), nullable=True)
    autores = Column(String(6000), nullable=True)       
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'EmpresaTecnologica({self.nombre}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac