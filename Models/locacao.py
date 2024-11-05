import datetime
from base import Base
from carro import Carro, Status
from reserva import Reserva, StatusLocacao  
from cliente import Cliente
from sqlalchemy import DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import NoResultFound
from pessoa import Locadora

engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()
class Locacao(Base):
    __tablename__ = 'locacao'
    
    id = Column(Integer, primary_key=True)
    data_alocacao = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    data_devolucao = Column(DateTime)
    valor_total = Column(Integer)
    reserva_id = Column(Integer, ForeignKey('reservas.id'))
    carro_placa = Column(String, ForeignKey('automovel.placa'))
    cliente_id = Column(Integer, ForeignKey('cliente.id_cliente'))
    reserva = relationship('Reserva', back_populates='locacoes')
    carro = relationship('Carro', backref='locacoes')
    cliente = relationship('Cliente')


    @property
    def calcular_valor_total(self):
        if self.data_devolucao and self.data_alocacao:
            dias_alugados = (self.data_devolucao - self.data_alocacao).days
            
            if dias_alugados < 1:
                dias_alugados = 1

            valor_total_calculado = self.carro.valor + (dias_alugados * self.carro.valor_diario)
            print(f'Dias alugados: {dias_alugados}, Valor diário: {self.carro.valor_diario}, Valor total calculado: {valor_total_calculado}')
            return valor_total_calculado
        return 0

Base.metadata.create_all(engine)

def alugar_carro():
    cpf_cliente = input("Digite o cpf do cliente: ")
    carro_placa = input("Digite a placa do carro: ")
    
    try:
        carro = session.query(Carro).filter_by(placa=carro_placa).one()
        if carro.status != Status.DISPONIVEL:
            print("Carro não disponível para aluguel.")
            return
        
        cliente = session.query(Cliente).filter_by(Cpf=cpf_cliente).one_or_none()
        if not cliente:
            print("Cliente não encontrado. Por favor, registre o cliente primeiro.")
            return
        
        reserva = Reserva(status=StatusLocacao.RESERVADO)
        session.add(reserva)
        session.commit()

        locacao = Locacao(
            reserva_id=reserva.id,
            carro_placa=carro.placa,
            cliente_id=cliente.id_cliente
        )
        
        carro.status = Status.ALUGADO
        
        session.add(locacao)
        session.commit()

        print(f"Carro {carro.placa} alugado com sucesso para o cliente {cliente.Nome}.")

    except NoResultFound:
        print("Carro ou reserva não encontrada.")
        session.rollback()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()
        
def devolver_carro():
    cpf_cliente = input("Digite o cpf do cliente: ")
    carro_placa = input("Digite a placa do carro alugado: ")
    try:
        cliente = session.query(Cliente).filter_by(Cpf=cpf_cliente).one_or_none()
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        locacao = session.query(Locacao).filter_by(cliente_id=cliente.id_cliente, carro_placa=carro_placa).all()
        if not locacao:
            print("Locação não encontrada para este cliente e carro.")
            return
        
        locacao = max(locacao, key=lambda l: l.data_alocacao)
        
        carro = session.query(Carro).filter_by(placa=carro_placa).one_or_none()
        if not carro:
            print("Carro não encontrado.")
            return
        
        reserva = session.query(Reserva).filter_by(id=locacao.reserva_id).one_or_none()
        if reserva:
            reserva.status = StatusLocacao.DEVOLVIDO

        carro.status = Status.DISPONIVEL
        
        locacao.data_devolucao = datetime.datetime.now(datetime.timezone.utc)
        
        session.commit()

        locacao.valor_total = locacao.calcular_valor_total
        session.commit()
        
        print(f"Carro {carro.placa} devolvido com sucesso pelo cliente {cliente.Nome}.")
        print(f"Valor total a pagar: R$ {locacao.calcular_valor_total:.2f}")
    
    except NoResultFound:
        print("Erro ao localizar carro ou locação.")
        session.rollback()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()


def main():
    while True:
        print('\nEscolha uma opção:')
        print('1. Alugar Automovel')
        print('2. Devolver Automoveis')
        print('3. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            alugar_carro()
        elif opcao == '2':
            devolver_carro()  
        elif opcao == '3':
            break
    
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()