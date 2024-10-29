from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Pessoa import Base  # Importa o Base e Locadora se necessário
from Funcionario import Funcionario  # Importa Funcionario para registrar a tabela
from Cliente import Cliente  # Importa Cliente para registrar a tabela

# Configura o banco de dados (exemplo com SQLite)
engine = create_engine('sqlite:///Locadoras.db')

# Cria as tabelas, se ainda não existirem
Base.metadata.create_all(engine)

# Cria uma sessão
Session = sessionmaker(bind=engine)
session = Session()

print("Tabelas 'Pessoa', 'Funcionario' e 'Cliente' criadas com sucesso.")






