from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Criação do engine e da sessão
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Carro(Base):
    __tablename__ = 'automovel'

    placa = Column(String, primary_key=True)
    cor = Column(String)
    marca = Column(String)
    modelo = Column(String)
    status = Column(String)
    valor = Column(Float)
    km = Column(Float)
    

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

def adicionar_automovel(placa,cor,  marca, modelo, valor, km):
    automovel = session.query(Carro).filter_by(placa = placa, cor=cor,  marca = marca, modelo = modelo, valor = valor, km = km).first()
    #Mudar o if pra verificar atraves da placa, evitando o não adicionamento de carros iguais
    if not automovel:
        automovel = Carro(placa = placa, cor=cor,  marca = marca, modelo = modelo, valor = valor, km = km)
        session.add(automovel)
        session.commit()


def consultar_automovel():
    automoveis = session.query(Carro).all()
    for automovel in automoveis:
        print(f"Cor: {automovel.cor}")
        print(f"Marca: {automovel.marca}")
        print(f"Modelo: {automovel.modelo}")
        print(f"Valor: {automovel.valor}")
        print(f"Quilometragem: {automovel.km}")

def remover_automovel(placa):
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if automovel:
        session.delete(automovel)
        session.commit()
        print(f"Automovel com placa {placa} removido com sucesso.")
    else:
        print(f"Automovel com placa {placa} não encontrado.")


        
def main():
    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Carro')
        print('2. Consultar Autores')
        print('3. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            placa = input('Placa: ')
            cor = input('Cor do Automovel: ')
            marca = input('Marca do Automovel: ')
            modelo = input('Modelo do Automovel: ')
            valor = input('Valor do Automovel: ')
            km = input('Quilometragem do Automovel: ')
            adicionar_automovel(placa, cor,  marca, modelo, valor, km)
        elif opcao == '2':
            consultar_automovel()
        elif opcao == '3':
            break
    
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()