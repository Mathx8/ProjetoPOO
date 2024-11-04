import enum
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from base import Base

# Criação do engine e da sessão
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class Status(enum.Enum):
    DISPONIVEL = "disponivel"
    ALUGADO = "alugado"
    EM_MANUNTENCAO = "em_manuntencao"
    FORA_DE_SERVICO = "fora_de_servico"
    

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

def adicionar_automovel():
    
    while True:
            placa = input('Placa: ').strip()
            if not placa:
                print("Por favor, preencha a placa.")
                continue

            cor = input('Cor do Automóvel: ').strip()
            if not cor:
                print("Por favor, preencha a cor do automóvel.")
                continue

            marca = input('Marca do Automóvel: ').strip()
            if not marca:
                print("Por favor, preencha a marca do automóvel.")
                continue

            modelo = input('Modelo do Automóvel: ').strip()
            if not modelo:
                print("Por favor, preencha o modelo do automóvel.")
                continue

            valor_input = input('Valor do Automóvel: ').strip()
            try:
                valor = float(valor_input)
                if valor <= 0:
                    print("Por favor, preencha um valor válido maior que zero.")
                    continue
            except ValueError:
                print("Por favor, insira um valor numérico válido para o valor do automóvel.")
                continue

            valor_diario_input = input('Valor Diário do Automóvel: ').strip()
            try:
                valor_diario = float(valor_diario_input)
                if valor_diario <= 0:
                    print("Por favor, preencha um valor diário válido maior que zero.")
                    continue
            except ValueError:
                print("Por favor, insira um valor numérico válido para o valor diário do automóvel.")
                continue

            km_input = input('Quilometragem do Automóvel: ').strip()
            try:
                km = float(km_input)
                if km <= 0:
                    print("Por favor, preencha uma quilometragem válida maior que zero.")
                    continue
            except ValueError:
                print("Por favor, insira um valor numérico válido para a quilometragem do automóvel.")
                continue
        
            

            automovel_existente = session.query(Carro).filter_by(placa=placa).first()
            if automovel_existente:
                print(f"Já existe um automóvel com a placa '{placa}'. Não foi possível adicionar.")
                continue

            salvar_automovel(placa, cor, marca, modelo, valor, valor_diario, km)
            break
    
def salvar_automovel(placa,cor,  marca, modelo, valor, valor_diario, km):
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
        if automovel.status is not None:
            print(f"Status: {automovel.status.value}")
        else:
            print("Status: Não definido")
        print("")

def remover_automovel(placa):
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if automovel:
        session.delete(automovel)
        session.commit()
        print(f"Automovel com placa '{placa}' removido com sucesso.")
    else:
        print(f"Automovel com placa '{placa}' não encontrado.")

def editar_automovel(placa):
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if automovel:
        print(f"Automóvel encontrado: {automovel.marca} {automovel.modelo} ({automovel.placa})")
        
        while True:
        # Coletar novas informações
            nova_cor = input(f'Nova cor (atual: {automovel.cor}): ').strip()
            if not nova_cor:
                    print("Por favor, preencha a marca do automóvel.")
                    continue
            novo_valor = input(f'Novo valor (atual: {automovel.valor}): ')
            try:
                valor = float(novo_valor)
                if valor <= 0:
                    print("Por favor, preencha um valor válido maior que zero.")
                    continue
            except ValueError:
                print("Por favor, insira um valor numérico válido para o valor do automóvel.")
                continue
            novo_valor_diario = input(f'Novo valor diario (atual: {automovel.valor_diario}): ')
            try:
                valor_diario = float(novo_valor_diario)
                if valor_diario <= 0:
                    print("Por favor, preencha um valor diário válido maior que zero.")
                    continue
            except ValueError:
                print("Por favor, insira um valor numérico válido para o valor diário do automóvel.")
                continue

            nova_km = input(f'Nova quilometragem (atual: {automovel.km}): ')
            try:
                km = float(nova_km)
                if km <= 0:
                    print("Por favor, preencha uma quilometragem válida maior que zero.")
                    continue
            except ValueError:
                print("Por favor, insira um valor numérico válido para a quilometragem do automóvel.")
                continue


            # Atualizar os atributos
            automovel.cor = nova_cor
            automovel.valor = float(novo_valor) if novo_valor else automovel.valor
            automovel.valor_diario = float(novo_valor_diario) if novo_valor_diario else automovel.valor_diario
            automovel.km = float(nova_km) 
            
            # Persistir as mudanças
            session.commit()
            print(f"Automóvel '{placa}' atualizado com sucesso.")
            break
    else:
        print(f"Automóvel com placa '{placa}' não encontrado.")

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
                automovel.status = Status.DISPONIVEL
                break
            elif opcao == '2':
                automovel.status = Status.ALUGADO
                break
            elif opcao == '3':
                automovel.status = Status.EM_MANUNTENCAO
                break
            elif opcao == '4':
                automovel.status = Status.FORA_DE_SERVICO
                break
            elif opcao == '5':
                break
        
            else:
                print('Opção inválida. Tente novamente.')
    else:
        
        print(f"Automovel com placa '{placa}' não encontrado.")
      
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
            adicionar_automovel()
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