import enum
from sqlalchemy import create_engine, Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class Status(enum.Enum):
    RESERVADO = "reservado"
    DEVOLVIDO = "devolvido"
    
Base = declarative_base()

class Reserva(Base):
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True)
    status = Column(Enum(Status), nullable=False)
    locacao_id = Column(Integer, ForeignKey('locacao.id'))
    locacao = relationship('Locacao', backref='reservas')
    
Base.metadata.create_all(engine)