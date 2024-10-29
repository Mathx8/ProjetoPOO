from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from base import Base

class Locadora(Base):
    __tablename__ = 'Pessoa'
    
    Cod_Usuario = Column(Integer, primary_key=True)
    Nome = Column(String)
    Idade = Column(Integer)
    Cpf = Column(String, unique=True)  # Adicionando a restrição unique
    DataNasc = Column(DateTime, nullable=False)
    
    def __init__(self, Nome, Idade, Cpf, DataNasc):
        self.Nome = Nome
        self.Idade = Idade
        self.Cpf = Cpf
        self.DataNasc = DataNasc

    def Validar_nome(self, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        self.Nome = nome

    def Validar_idade(self, idade):
        if not isinstance(idade, int) or idade < 18:
            raise ValueError("Idade inválida, deve ser um número inteiro positivo e maior que 18 anos.")
        self.Idade = idade

    def Validar_Cpf(self, cpf, session):
        if not (cpf.isdigit() and len(cpf) == 11):
            raise ValueError("CPF inválido, deve conter 11 dígitos.")
        
        cpf_existente = session.query(Locadora).filter_by(Cpf=cpf).first()
        if cpf_existente:
            raise ValueError(f"Erro: CPF '{cpf}' já está cadastrado.")
        
        self.Cpf = cpf 

    def Validar_DataNasc(self, dataNasc):
        try:
            data = datetime.strptime(dataNasc, '%Y-%m-%d')
            if data >= datetime.now():
                raise ValueError("Data de nascimento não pode ser no futuro.")
            self.DataNasc = data
        except ValueError:
            raise ValueError("Data de nascimento inválida, use o formato YYYY-MM-DD e certifique-se de que não está no futuro.")

    @staticmethod
    def adicionar_locadora(session, nome, idade, cpf, data_nasc):
        try:
            nova_Locadora = Locadora(nome, idade, cpf, data_nasc)
            nova_Locadora.Validar_nome(nome)
            nova_Locadora.Validar_idade(idade)
            nova_Locadora.Validar_Cpf(cpf, session)
            nova_Locadora.Validar_DataNasc(data_nasc)
            
            session.add(nova_Locadora)
            session.commit()
            return f"Usuário '{nome}' adicionado com sucesso."
        except ValueError as e:
            return f"Erro ao adicionar usuário: {e}"
