from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from base import Base
from Erros import DataNascFuturaException, DataNascFormatException
from Erros import IdadeInvalidaException, IdadeMinimaException, CpfInvalidoException, CpfExistenteException

class Locadora(Base):
    __tablename__ = 'Pessoa'
    
    Cod_Usuario = Column(Integer, primary_key=True)
    Nome = Column(String)
    Idade = Column(Integer)
    Cpf = Column(String, unique=True)
    DataNasc = Column(DateTime, nullable=False)
    
    def __init__(self, Nome, Idade, Cpf, DataNasc):
        self.Nome = Nome
        self.Idade = Idade
        self.Cpf = Cpf
        self.DataNasc = DataNasc

    def Validar_nome(self, nome):
        if not nome or len(nome) < 3:
            raise ValueError("Nome deve conter Min. 3 caracteres.")
        self.Nome = nome

    def Validar_idade(self, idade):
        try:
            idade = int(idade)
            if idade < 0:
                raise IdadeInvalidaException
            if idade < 18:  
                raise IdadeMinimaException
            self.Idade = idade
        except ValueError:
            raise IdadeInvalidaException

    def Validar_Cpf(self, cpf, session):
        try:
            if not (cpf.isdigit() and len(cpf) == 11):
                raise CpfInvalidoException
            
            cpf_existente = session.query(Locadora).filter_by(Cpf=cpf).first()
            if cpf_existente:
                raise CpfExistenteException
            self.Cpf = cpf
        except (CpfInvalidoException, CpfExistenteException) as e:
            raise e

    def Validar_DataNasc(self, dataNasc):
        try:  
            # Converte dataNasc para datetime no formato DD/MM/YYYY
            if isinstance(dataNasc, str):
                dataNasc = datetime.strptime(dataNasc, '%d/%m/%Y')
                
            # Verifica se a data está no futuro
            if dataNasc > datetime.now():
                raise DataNascFuturaException
            self.DataNasc = dataNasc
            
        except ValueError:
            raise DataNascFormatException
        
        except DataNascFuturaException as e:  
            raise e

    @staticmethod
    def adicionar_locadora(session, nome, idade, cpf, data_nasc):
        try:
            nova_Locadora = Locadora(nome, idade, cpf, None)
            nova_Locadora.Validar_nome(nome)
            nova_Locadora.Validar_idade(idade)
            nova_Locadora.Validar_Cpf(cpf, session)
            nova_Locadora.Validar_DataNasc(data_nasc)

            session.add(nova_Locadora)
            session.commit()
            return f"Usuário '{nome}' adicionado com sucesso."
        except Exception as e:
            return f"Ocorreu um erro inesperado: {e}"
