from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class Basico(Base):
    
    __tablename__ = 'basico'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    nombre = Column(String(800), nullable=True)
    fecha_formacion = Column(String(500), nullable=True)
    lugar = Column(String(200), nullable=False)
    lider = Column(String(400), nullable=True)
    certificacion = Column(String(200), nullable=True)
    pagina_web = Column(String(300), nullable=True)
    email = Column(String(150), nullable=True)
    clasificacion = Column(String(300), nullable=True)
    areas = Column(String(3000), nullable=True)
    programas = Column(String(3000), nullable=True)
    programas_secundario = Column(String(2000), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Basico({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac