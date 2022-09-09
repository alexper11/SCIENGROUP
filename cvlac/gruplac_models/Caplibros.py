from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, Boolean

class Caplibros(Base):
    
    __tablename__ = 'caplibros'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    verificado = Column(Boolean,unique=False, default=True)
    tipo = Column(String(100), nullable=True)
    capitulo = Column(String(200), nullable=True)
    lugar = Column(String(80), nullable=True)
    fecha = Column(String(70), nullable=True)
    libro = Column(String(200), nullable=True)
    isbn = Column(String(60), nullable=True)
    volumen = Column(String(200), nullable=True)
    paginas = Column(String(50), nullable=True)
    editorial = Column(String(100), nullable=True)
    autores = Column(String(3000), nullable=True)       
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Caplibros({self.capitulo}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac