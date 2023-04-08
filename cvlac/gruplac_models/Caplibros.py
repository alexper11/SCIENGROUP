from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Caplibros(Base):
    
    __tablename__ = 'caplibros'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), ForeignKey("basico.idgruplac"), nullable=False)
    verificado = Column(Boolean,unique=False, default=True)
    tipo = Column(String(150), nullable=True)
    capitulo = Column(String(1500), nullable=True)
    lugar = Column(String(200), nullable=True)
    fecha = Column(String(100), nullable=True)
    libro = Column(String(1500), nullable=True)
    isbn = Column(String(200), nullable=True)
    volumen = Column(String(200), nullable=True)
    paginas = Column(String(50), nullable=True)
    editorial = Column(String(1000), nullable=True)
    autores = Column(String(3000), nullable=True)       
    
    basico = relationship('Basico', backref='caplibros')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Caplibros({self.capitulo}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac