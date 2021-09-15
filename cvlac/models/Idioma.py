from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Idioma(Base):
    
    __tablename__ = 'idioma'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    idioma = Column(String(30), nullable=False)
    habla = Column(String(30), nullable=False)
    escribe = Column(String(30), nullable=False)
    lee = Column(String(30), nullable=False)
    entiende = Column(String(30), nullable=False)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Idioma({self.idioma}, {self.entiende}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac