from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from pessoa import Locadora, Base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
#Interface
import tkinter as tk
from tkinter import messagebox


class Funcionario(Locadora):
    __tablename__ = 'funcionario'

    id_funcionario = Column(Integer, primary_key=True)
    Funcao = Column(String)
    cod_usuario = Column(Integer, ForeignKey('Pessoa.Cod_Usuario'))  

    def __init__(self, Nome, Idade, Cpf, DataNasc, Funcao):
        super().__init__(Nome, Idade, Cpf, DataNasc)
        self.Funcao = Funcao

    def Validar_funcao(self, funcao):
        if not funcao:
            raise ValueError("Função não pode ser vazia.")
        self.Funcao = funcao

def adicionar_funcionario(session, nome, idade, cpf, data_nasc, funcao):
    try:
        data_nasc = datetime.strptime(data_nasc, '%Y-%m-%d')
        
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
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"

# Configura o banco de dados (exemplo com SQLite)
engine = create_engine('sqlite:///locadora.db')
Base.metadata.create_all(engine)
 
# Configura o banco de dados (exemplo com SQLite)
engine = create_engine('sqlite:///locadora.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def adicionar_funcionario_interface():
    nome = entry_nome.get()
    idade = entry_idade.get()
    cpf = entry_cpf.get()
    data_nasc = entry_data_nasc.get()
    funcao = entry_funcao.get()


    try:
        # Converte idade para inteiro
        idade = int(idade)


        # Chama a função para adicionar o cliente
        resultado = adicionar_funcionario(session, nome, idade, cpf, data_nasc, funcao)
        messagebox.showinfo("Sucesso", resultado)

        # Limpa os campos após adicionar
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_data_nasc.delete(0, tk.END)
        entry_funcao.delete(0, tk.END)
        

    except ValueError as ve:
        messagebox.showerror("Erro de Valor", f"Erro nos valores fornecidos: {ve}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    # Criação da janela principal
    root = tk.Tk()
    root.title("Cadastro de Clientes")

    # Definindo os rótulos e campos de entrada
    tk.Label(root, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=0, column=1)

    tk.Label(root, text="Idade:").grid(row=1, column=0)
    entry_idade = tk.Entry(root)
    entry_idade.grid(row=1, column=1)

    tk.Label(root, text="CPF:").grid(row=2, column=0)
    entry_cpf = tk.Entry(root)
    entry_cpf.grid(row=2, column=1)

    tk.Label(root, text="Data de Nascimento:").grid(row=3, column=0)
    entry_data_nasc = tk.Entry(root)
    entry_data_nasc.grid(row=3, column=1)

    tk.Label(root, text="Funçao:").grid(row=4, column=0)
    entry_funcao = tk.Entry(root)
    entry_funcao.grid(row=4, column=1)



    # Botão para adicionar cliente
    btn_adicionar = tk.Button(root, text="Adicionar Funcionario", command=adicionar_funcionario_interface)
    btn_adicionar.grid(row=8, column=0, columnspan=2)

    # Inicia o loop da interface
    root.mainloop()

'''# Cria uma sessão
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
session.close()'''

