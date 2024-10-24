import enum
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Criação do engine e da sessão
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class Status(enum.Enum):
    DISPONIVEL = "disponivel"
    ALUGADO = "alugado"
    EM_MANUNTENCAO = "em_manuntencao"
    FORA_DE_SERVICO = "fora_de_servico"
    

Base = declarative_base()



class Carro(Base):
    __tablename__ = 'automovel'

    placa = Column(String, primary_key=True)
    cor = Column(String)
    marca = Column(String)
    modelo = Column(String)
    valor = Column(Float)
    valor_diario = Column(Float)
    km = Column(Float)
    status = Column(Enum(Status))
    

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

def adicionar_automovel(placa,cor,  marca, modelo, valor, valor_diario, km):
    automovel = session.query(Carro).filter_by(placa = placa, cor=cor,  marca = marca, modelo = modelo, valor = valor, valor_diario = valor_diario, km = km).first()
    #Mudar o if pra verificar atraves da placa, evitando o não adicionamento de carros iguais
    if not automovel:
        automovel = Carro(placa = placa, cor=cor,  marca = marca, modelo = modelo, valor = valor, valor_diario = valor_diario, km = km)
        session.add(automovel)
        session.commit()


def consultar_automovel():
    automoveis = session.query(Carro).all()
    for automovel in automoveis:
        print("")
        print(f"Placa: {automovel.placa}")
        print(f"Cor: {automovel.cor}")
        print(f"Marca: {automovel.marca}")
        print(f"Modelo: {automovel.modelo}")
        print(f"Valor: {automovel.valor}")
        print(f"Valor diario: {automovel.valor_diario}")
        print(f"Quilometragem: {automovel.km}")
        print(f"Status: {automovel.status}")
        print("")

def remover_automovel(placa):
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if automovel:
        session.delete(automovel)
        session.commit()
        print(f"Automovel com placa {placa} removido com sucesso.")
    else:
        print(f"Automovel com placa {placa} não encontrado.")

def editar_automovel(placa):
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if automovel:
        print(f"Automóvel encontrado: {automovel.marca} {automovel.modelo} ({automovel.placa})")
        
        # Coletar novas informações
        nova_cor = input(f'Nova cor (atual: {automovel.cor}): ')
        novo_valor = input(f'Novo valor (atual: {automovel.valor}): ')
        novo_valor_diario = input(f'Novo valor diario (atual: {automovel.valor_diario}): ') 
        nova_km = input(f'Nova quilometragem (atual: {automovel.km}): ') 
        
        # Atualizar os atributos
        automovel.cor = nova_cor
        automovel.valor = float(novo_valor) if novo_valor else automovel.valor
        automovel.valor_diario = float(novo_valor_diario) if novo_valor_diario else automovel.valor_diario
        automovel.km = float(nova_km) 
        
        # Persistir as mudanças
        session.commit()
        print(f"Automóvel {placa} atualizado com sucesso.")
    else:
        print(f"Automóvel com placa {placa} não encontrado.")


def status(placa):
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if automovel:
        print(f"Automóvel encontrado: {automovel.marca} {automovel.modelo} ({automovel.status})")

        
        while True:
            print('\nEscolha o status do automovel:')
            print('1. Disponivel')
            print('2. Alugado')
            print('3. Em manuntencao')
            print('4. Fora de servico')
            print('5. Sair')

            opcao = input('Opção: ')
            if opcao == '1':
                automovel.status = "disponivel"
                
            elif opcao == '2':
                automovel.status = "alugado"
            elif opcao == '3':
                automovel.status = "em_manuntencao"
            elif opcao == '4':
                automovel.status = "fora_de_servico"
            elif opcao == '5':
                break
        
            else:
                print('Opção inválida. Tente novamente.')
        

        
def main():
    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Automovel')
        print('2. Consultar Automoveis')
        print('3. Remover Automovel')
        print('4. Editar Automovel')
        print('5. Editar Status do Automovel')
        print('6. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            placa = input('Placa: ')
            cor = input('Cor do Automovel: ')
            marca = input('Marca do Automovel: ')
            modelo = input('Modelo do Automovel: ')
            valor = float(input('Valor do Automovel: '))
            valor_diario = float(input('Valor Diario do Automovel: '))
            km = float(input('Quilometragem do Automovel: '))
            adicionar_automovel(placa, cor,  marca, modelo, valor, valor_diario,  km)
        elif opcao == '2':
            consultar_automovel()
        elif opcao == '3':
            placa_remover = input("Digite a placa do automovel a ser removido: ")
            remover_automovel(placa_remover)
        elif opcao == '4':
            placa_editar = input("Digite a placa do automovel a ser editado: ")
            editar_automovel(placa_editar)
        elif opcao == '5':
            placa_status = input("Digite a placa do automovel a ser trocado o status: ")
            status(placa_status)   
        elif opcao == '6':
            break
    
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()