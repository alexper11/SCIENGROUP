from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class Basico(Base):
    
    __tablename__ = 'basico'
    #id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), primary_key=True)
    nombre = Column(String(1500), nullable=True)
    fecha_formacion = Column(String(500), nullable=True)
    lugar = Column(String(300), nullable=True)
    lider = Column(String(1500), nullable=True)
    certificacion = Column(String(500), nullable=True)
    pagina_web = Column(String(1000), nullable=True)
    email = Column(String(250), nullable=True)
    clasificacion = Column(String(600), nullable=True)
    areas = Column(String(3000), nullable=True)
    programas = Column(String(3000), nullable=True)
    programas_secundario = Column(String(3000), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Basico({self.nombre}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac