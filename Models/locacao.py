import datetime
from .carro import Carro
from .reserva import Reserva, Status  
from .cliente import Cliente
from sqlalchemy import DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.exc import NoResultFound

engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Locacao(Base):
    __tablename__ = 'locacao'
    
    id = Column(Integer, primary_key=True)
    data_alocacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_devolucao = Column(DateTime)
    valor_total = Column(Carro.valor * (Carro.valor_diario+(data_devolucao-data_alocacao)))
    reserva_id = Column(Integer, ForeignKey('reservas.id'))
    carro_placa = Column(String, ForeignKey('automovel.placa'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    reserva = relationship('Reserva', backref='locacao')
    carro = relationship('Carro', backref='locacao')
    cliente = relationship('Cliente', backref='locacao')

Base.metadata.create_all(engine)

def alugar_carro(session):
    nome_cliente = input("Digite o nome do cliente: ")
    carro_placa = input("Digite a placa do carro: ")
    
    try:
        carro = session.query(Carro).filter_by(placa=carro_placa).one()
        if carro.status != "DISPONÍVEL":
            print("Carro não disponível para aluguel.")
            return
        
        cliente = session.query(Cliente).filter_by(nome=nome_cliente).one_or_none()
        if not cliente:
            print("Cliente não encontrado. Por favor, registre o cliente primeiro.")
            return
        
        reserva = Reserva(status=Status.RESERVADO)
        session.add(reserva)
        session.commit()

        locacao = Locacao(
            reserva_id=reserva.id,
            carro_placa=carro.placa,
            cliente_id=cliente.id
        )
        
        carro.status
        
        session.add(locacao)
        session.commit()

        print(f"Carro {carro.placa} alugado com sucesso para o cliente {cliente.nome}.")

    except NoResultFound:
        print("Carro ou reserva não encontrada.")
        session.rollback()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()
        
def devolver_carro(session):
    nome_cliente = input("Digite o nome do cliente: ")
    carro_placa = input("Digite a placa do carro alugado: ")
    try:
        cliente = session.query(Cliente).filter_by(nome=nome_cliente).one_or_none()
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        locacao = session.query(Locacao).filter_by(cliente_id=cliente.id, carro_placa=carro_placa).one_or_none()
        if not locacao:
            print("Locação não encontrada para este cliente e carro.")
            return
        
        carro = session.query(Carro).filter_by(placa=carro_placa).one()
        carro.status = "DISPONÍVEL"
        
        locacao.data_devolucao = datetime.datetime.utcnow()
        
        session.commit()
        
        print(f"Carro {carro.placa} devolvido com sucesso pelo cliente {cliente.nome}.")
        print(f"Valor total a pagar: R$ {Locacao.valor_total:.2f}")
    
    except NoResultFound:
        print("Erro ao localizar carro ou locação.")
        session.rollback()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()