import datetime
import decimal
from .carro import Carro
from .reserva import Reserva  
from .cliente import Cliente
from sqlalchemy import DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Locacao(Base):
    __tablename__ = 'locacao'
    
    id = Column(Integer, primary_key=True)
    data_alocacao = Column(DateTime, default=datetime.utcnow)
    data_devolucao = Column(DateTime)
    valor_total = Column(decimal)
    reserva_id = Column(Integer, ForeignKey('reservas.id'))
    carro_placa = Column(String, ForeignKey('automovel.placa'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    reserva = relationship('Reserva', backref='locacao')
    carro = relationship('Carro', backref='locacao')
    cliente = relationship('Cliente', backref='locacao')

Base.metadata.create_all(engine)

def AlugarCarro(session, cliente_id, carro_placa, reserva_id):
    carro = session.query(Carro).filter_by(placa=carro_placa).first()
    if not carro or carro.status != StatusCarro.DISPONÍVEL:
        print("Carro não disponível para aluguel.")
        return
