from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, Boolean

class EmpresaTecnologica(Base):
    
    __tablename__ = 'empresa_tecnologica'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    autores = Column(String(4000), nullable=False)
    nombre = Column(String(1000), nullable=False)
    tipo = Column(String(500), nullable=False)
    nit = Column(String(50), nullable=False)
    registro_camara = Column(String(300), nullable=True)
    verificado = Column(Boolean,unique=False, default=True)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'EmpresaTecnologica({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac