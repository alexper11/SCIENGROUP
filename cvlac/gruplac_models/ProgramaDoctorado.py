from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class ProgramaDoctorado(Base):
    
    __tablename__ = 'programa_doctorado'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), ForeignKey("basico.idgruplac"), nullable=False)
    programa = Column(String(600), nullable=True)
    fecha = Column(String(60), nullable=True)
    acto = Column(String(400), nullable=True)
    institucion = Column(String(600), nullable=True)
    
    basico = relationship('Basico', backref='programa_doctorado')
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'ProgramaDoctorado({self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac