from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pessoa import Base  # Importa o Base e Locadora se necessário
from funcionario import Funcionario  # Importa Funcionario para registrar a tabela
from cliente import Cliente  # Importa Cliente para registrar a tabela
import reserva
import carro
from locacao import Locacao
from base import Base

# Configura o banco de dados (exemplo com SQLite)
engine = create_engine('sqlite:///locadora.db')

# Cria uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Cria as tabelas, se ainda não existirem
Base.metadata.create_all(engine)

print("Tabelas 'Pessoa', 'Funcionario' e 'Cliente' criadas com sucesso.")
