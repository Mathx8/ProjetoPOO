from sqlalchemy import Column, Integer, String, ForeignKey, DateTime  # Importando DateTime do SQLAlchemy
from Pessoa import Locadora, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class Cliente(Locadora): 
    __tablename__ = 'Cliente'

    id_cliente = Column(Integer, primary_key=True)
    Numero_Carteira = Column(Integer, nullable=False)  
    Categoria = Column(String, nullable=False)  
    Data_Emissao = Column(DateTime, nullable=False)  
    Data_Validade = Column(DateTime, nullable=False)  
    cod_cliente = Column(Integer, ForeignKey('Pessoa.Cod_Usuario'), nullable=False)

    def __init__(self, Nome, Idade, Cpf, DataNasc, Numero_Carteira, Categoria, Data_Emissao, Data_Validade):
        super().__init__(Nome, Idade, Cpf, DataNasc)
        self.Numero_Carteira = Numero_Carteira
        self.Categoria = Categoria
        self.Data_Emissao = Data_Emissao
        self.Data_Validade = Data_Validade

    def Validar_Numero_Carteira(self, numero_Carteira):
        if not (str(numero_Carteira).isdigit() and len(str(numero_Carteira)) == 11):
            raise ValueError("O Número da carteira de motorista inválido, deve conter 11 dígitos.")
        self.Numero_Carteira = numero_Carteira

    def Validar_Data_Emissao(self, data_Emissao):
        if data_Emissao >= datetime.now():
            raise ValueError("Data de emissão não pode ser no futuro.")
        self.Data_Emissao = data_Emissao

    def Validar_Data_Validade(self, data_Validade):
        if data_Validade <= datetime.now():
            raise ValueError("Data de validade deve ser uma data futura.")
        self.Data_Validade = data_Validade

def adicionar_cliente(session, nome, idade, cpf, data_nasc, numero_carteira, categoria, data_emissao, data_validade):
    try:
        # Converte as datas para `datetime`
        data_nasc = datetime.strptime(data_nasc, '%Y-%m-%d')
        data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d')
        data_validade = datetime.strptime(data_validade, '%Y-%m-%d')

        novo_cliente = Cliente(nome, idade, cpf, data_nasc, numero_carteira, categoria, data_emissao, data_validade)

        # Chamando as validações
        novo_cliente.Validar_nome(nome)
        novo_cliente.Validar_idade(idade)
        novo_cliente.Validar_Cpf(cpf, session)
        novo_cliente.Validar_Numero_Carteira(numero_carteira)
        novo_cliente.Validar_Data_Emissao(data_emissao)
        novo_cliente.Validar_Data_Validade(data_validade)

        session.add(novo_cliente)
        session.commit()
        return f"Cliente '{nome}' adicionado com sucesso."
    except ValueError as e:
        return f"Erro ao adicionar cliente: {e}"

# Configura o banco de dados
engine = create_engine('sqlite:///Locadoras.db')
Base.metadata.create_all(engine)

# Cria uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Adiciona cinco clientes
cliente1 = adicionar_cliente(session, "Ana Clara", 25, "12345678909", "1998-01-15", '12345678901', "A", "2024-01-01", "2030-01-01")
print(cliente1)
cliente2 = adicionar_cliente(session, "Bruno Oliveira", 27, "98765432100", "1996-05-20", '22345678901', "B", "2024-02-01", "2030-02-01")
print(cliente2)
cliente3 = adicionar_cliente(session, "Carlos Eduardo", 29, "11122233344", "1994-10-10", '33345678901', "C", "2024-03-01", "2030-03-01")
print(cliente3)
cliente4 = adicionar_cliente(session, "Fernanda Lima", 26, "44455566677", "1997-03-30", '44445678901', "D", "2024-04-01", "2030-04-01")
print(cliente4)
cliente5 = adicionar_cliente(session, "Lucas Martins", 28, "88899900011", "1995-12-25", '55545678901', "E", "2024-05-01", "2030-05-01")
print(cliente5)

# Fecha a sessão
session.close()

print("Cinco clientes foram adicionados com sucesso.")
