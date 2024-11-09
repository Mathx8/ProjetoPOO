from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pessoa import Base  
from funcionario import Funcionario  
from cliente import Cliente
from reserva import Reserva
from locacao import Locacao
from carro import Carro 
import pandas as pd
import reserva
import carro
from locacao import Locacao
from base import Base

engine = create_engine('sqlite:///locadora.db')

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

'''Pessoa = pd.read_sql_table("Pessoa", con=engine)


print(Pessoa)'''
