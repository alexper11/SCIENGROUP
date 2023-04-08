from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Idioma(Base):
    
    __tablename__ = 'idioma'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    idioma = Column(String(80), nullable=True)
    habla = Column(String(80), nullable=True)
    escribe = Column(String(80), nullable=True)
    lee = Column(String(80), nullable=True)
    entiende = Column(String(80), nullable=True)
    
    basico = relationship('Basico', backref='idioma')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Idioma({self.idioma}, {self.entiende}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac