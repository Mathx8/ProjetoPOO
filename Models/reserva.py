import enum
from sqlalchemy import create_engine, Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from base import Base

engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class StatusLocacao(enum.Enum):
    RESERVADO = "reservado"
    DEVOLVIDO = "devolvido"    

class Reserva(Base):
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True)
    status = Column(Enum(StatusLocacao))

    locacao = relationship('Locacao', backref='reservas')
    
Base.metadata.create_all(engine)