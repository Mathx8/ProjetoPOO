from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from pessoa import Locadora, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from Erros import DataNascFuturaException, DataNascFormatException
from Erros import IdadeInvalidaException,IdadeMinimaException, CpfExistenteException,CpfInvalidoException

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
        
        data_nasc = datetime.strptime(data_nasc, '%d/%m/%Y')


        novo_funcionario = Funcionario(nome, idade, cpf, data_nasc,funcao)

        # Chamando as validações em ordem
        novo_funcionario.Validar_nome(nome)
        novo_funcionario.Validar_idade(idade)
        novo_funcionario.Validar_Cpf(cpf, session)
        novo_funcionario.Validar_funcao(funcao)
      

        session.add(novo_funcionario)
        session.commit()
        return f"funcionario '{nome}' adicionado com sucesso."
    except ValueError as e:
        return f"Erro ao adicionar funcionario: {e}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"

# Configura o banco de dados
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
  
        novo_funcionario = Funcionario(nome, idade, cpf,data_nasc,funcao)

        # Chamando as validações em ordem
        novo_funcionario.Validar_nome(nome)
        novo_funcionario.Validar_idade(idade)
        novo_funcionario.Validar_Cpf(cpf, session)
        novo_funcionario.Validar_DataNasc(datetime.strptime(data_nasc, '%d/%m/%Y'))
        novo_funcionario.Validar_funcao(funcao)

        
        session.add(novo_funcionario)
        session.commit()
        messagebox.showinfo("Resultado", f"funcionario '{nome}' adicionado com sucesso.")

        # Limpa os campos após adicionar
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_data_nasc.delete(0, tk.END)
        entry_funcao.delete(0, tk.END)

        
        # Erros Data
    except DataNascFuturaException as dt:
        messagebox.showerror("Erro de Data", str(dt))
    except DataNascFormatException as dt:
        messagebox.showerror("Erro de Data", str(dt))
        # Erros Idade
    except IdadeInvalidaException as i:
        messagebox.showerror("Erro de Idade", str(i))
    except IdadeMinimaException as i:
        messagebox.showerror("Erro de Idade", str(i))
        # Erros CPF
    except CpfExistenteException as cp:
            messagebox.showerror("Erro de Cpf", str(cp))   
    except CpfInvalidoException as cp:
            messagebox.showerror("Erro de Cpf", str(cp))
        #Value erro
    except ValueError as e:
        messagebox.showerror("Erro:", str(e))
        #Erro desconhecido 
    except Exception as e:
        messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cadastro de funcionarios")

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

    tk.Label(root, text="Função:").grid(row=4, column=0)
    entry_funcao = tk.Entry(root)
    entry_funcao.grid(row=4, column=1)


    # Botão para adicionar funcionario
    btn_adicionar = tk.Button(root, text="Adicionar funcionario", command=adicionar_funcionario_interface)
    btn_adicionar.grid(row=8, column=0, columnspan=2)

    # Inicia o loop da interface
    root.mainloop()
