import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cliente import adicionar_cliente  # Assegure-se de que a função está corretamente importada

# Configuração do banco de dados
engine = create_engine('sqlite:///locadora.db')
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
        # Converte idade para inteiro
        idade = int(idade)

        # Converte as datas para objetos `datetime`
        data_nasc = datetime.strptime(data_nasc, '%Y-%m-%d')
        data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d')
        data_validade = datetime.strptime(data_validade, '%Y-%m-%d')

        # Chama a função para adicionar o cliente
        resultado = adicionar_cliente(session, nome, idade, cpf, data_nasc, numero_carteira, categoria, data_emissao, data_validade)
        messagebox.showinfo("Sucesso", resultado)

        # Limpa os campos após adicionar
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_data_nasc.delete(0, tk.END)
        entry_numero_carteira.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
        entry_data_emissao.delete(0, tk.END)
        entry_data_validade.delete(0, tk.END)

    except ValueError as ve:
        messagebox.showerror("Erro de Valor", f"Erro nos valores fornecidos: {ve}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


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


