from sqlalchemy import Column, Integer, String, ForeignKey
from Pessoa import Locadora, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Funcionario(Locadora):
    __tablename__ = 'Funcionario'

    id_funcionario = Column(Integer, primary_key=True)
    Funcao = Column(String)
    cod_usuario = Column(Integer, ForeignKey('Pessoa.Cod_Usuario'))  # Chave estrangeira

    def __init__(self, Nome, Idade, Cpf, DataNasc, Funcao):
        super().__init__(Nome, Idade, Cpf, DataNasc)
        self.Funcao = Funcao

    def Validar_funcao(self, funcao):
        if not funcao:
            raise ValueError("Função não pode ser vazia.")
        self.Funcao = funcao

def adicionar_funcionario(session, nome, idade, cpf, data_nasc, funcao):
    try:
            novo_funcionario = Funcionario(nome, idade, cpf, data_nasc, funcao)
            novo_funcionario.Validar_nome(nome)
            novo_funcionario.Validar_idade(idade)
            novo_funcionario.Validar_Cpf(cpf, session)
            novo_funcionario.Validar_DataNasc(data_nasc)
            novo_funcionario.Validar_funcao(funcao)

            session.add(novo_funcionario)
            session.commit()
            return f"Funcionário '{nome}' adicionado com sucesso."
    except ValueError as e:
            return f"Erro ao adicionar funcionário: {e}"
  
# Configura o banco de dados (exemplo com SQLite)
engine = create_engine('sqlite:///Locadoras.db')
Base.metadata.create_all(engine)

# Cria uma sessão
Session = sessionmaker(bind=engine)
session = Session()
    

funcionario1 = adicionar_funcionario(session,"João Pereira", 25, "11111111111", "1998-01-15", "Gerente")
print(funcionario1)
funcionario2 = adicionar_funcionario(session,"Maria Souza", 27, "22222222222", "1996-05-20", "Atendente")
print(funcionario2)
funcionario3 = adicionar_funcionario(session,"Carlos Silva", 29, "33333333333", "1994-10-10", "Supervisor")
print(funcionario3)
funcionario4 = adicionar_funcionario(session,"Ana Oliveira", 26, "44444444444", "1997-03-30", "Auxiliar")
print(funcionario4)
funcionario5 = adicionar_funcionario(session,"Luciana Santos", 28, "55555555555", "1995-12-25", "Vendedora")
print(funcionario5)
        
# Confirma a adição no banco de dados
session.commit()

print("Cinco funcionários foram adicionados com sucesso.")

# Fecha a sessão
session.close()