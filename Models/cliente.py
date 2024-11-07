from sqlalchemy import Column, Integer, String, ForeignKey, DateTime 
from pessoa import Locadora, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from Erros import DataNascFuturaException, DataNascFormatException
from Erros import IdadeInvalidaException,IdadeMinimaException, CpfExistenteException,CpfInvalidoException

class Cliente(Locadora): 
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True)
    Numero_Carteira = Column(Integer, nullable=False)  
    Categoria = Column(String, nullable=False)  
    Data_Emissao = Column(DateTime, nullable=False)  
    Data_Validade = Column(DateTime, nullable=False)  
    cod_cliente = Column(Integer, ForeignKey('Pessoa.Cod_Usuario'), nullable=False)

    def __init__(self, Nome, idade, Cpf, DataNasc, Numero_Carteira, Categoria, Data_Emissao, Data_Validade):
        super().__init__(Nome, idade, Cpf, DataNasc)
        self.Numero_Carteira = Numero_Carteira
        self.Categoria = Categoria
        self.Data_Emissao = Data_Emissao
        self.Data_Validade = Data_Validade

    def Validar_Numero_Carteira(self, numero_Carteira):
        if not (str(numero_Carteira).isdigit() and len(str(numero_Carteira)) == 11):
            raise ValueError("O Número da carteira de motorista inválido, deve conter 11 dígitos.")
        self.Numero_Carteira = numero_Carteira
    
    def Validar_categoria(self, categoria):
        if not categoria:
            raise ValueError("Categoria não pode ser vazio.")
        self.Categoria = categoria

    def Validar_Data_Emissao(self, data_Emissao):
        if data_Emissao >= datetime.now():
            raise DataNascFuturaException
        
        self.Data_Emissao = data_Emissao

    def Validar_Data_Validade(self, data_Validade):
        if data_Validade <= datetime.now():
            raise ValueError("Data de validade deve ser uma data futura.")
        self.Data_Validade = data_Validade



# Configura o banco de dados
engine = create_engine('sqlite:///locadora.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def adicionar_cliente_interface():
    nome = entry_nome.get()
    idade = entry_idade.get()
    cpf = entry_cpf.get()
    data_nasc = entry_data_nasc.get()
    numero_carteira = entry_numero_carteira.get()
    categoria = entry_categoria.get()
    data_emissao = entry_data_emissao.get()
    data_validade = entry_data_validade.get()

    try:
  
        novo_cliente = Cliente(nome, idade, cpf,data_nasc,numero_carteira, categoria,data_emissao,data_validade)

        # Chamando as validações em ordem
        novo_cliente.Validar_nome(nome)
        novo_cliente.Validar_idade(idade)
        novo_cliente.Validar_Cpf(cpf, session)
        novo_cliente.Validar_DataNasc(datetime.strptime(data_nasc, '%d/%m/%Y'))
        novo_cliente.Validar_Numero_Carteira(numero_carteira)
        novo_cliente.Validar_categoria(categoria)
        novo_cliente.Validar_Data_Emissao(datetime.strptime(data_emissao, '%d/%m/%Y'))
        novo_cliente.Validar_Data_Validade(datetime.strptime(data_validade, '%d/%m/%Y'))
        
        session.add(novo_cliente)
        session.commit()
        messagebox.showinfo("Resultado", f"Cliente '{nome}' adicionado com sucesso.")

        # Limpa os campos após adicionar
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_data_nasc.delete(0, tk.END)
        entry_numero_carteira.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
        entry_data_emissao.delete(0, tk.END)
        entry_data_validade.delete(0, tk.END)
        
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

    tk.Label(root, text="Número da Carteira:").grid(row=4, column=0)
    entry_numero_carteira = tk.Entry(root)
    entry_numero_carteira.grid(row=4, column=1)

    tk.Label(root, text="Categoria:").grid(row=5, column=0)
    entry_categoria = tk.Entry(root)
    entry_categoria.grid(row=5, column=1)

    tk.Label(root, text="Data de Emissão:").grid(row=6, column=0)
    entry_data_emissao = tk.Entry(root) 
    entry_data_emissao.grid(row=6, column=1)

    tk.Label(root, text="Data de Validade:").grid(row=7, column=0)
    entry_data_validade = tk.Entry(root)
    entry_data_validade.grid(row=7, column=1)

    # Botão para adicionar cliente
    btn_adicionar = tk.Button(root, text="Adicionar Cliente", command=adicionar_cliente_interface)
    btn_adicionar.grid(row=8, column=0, columnspan=2)

    # Inicia o loop da interface
    root.mainloop()
