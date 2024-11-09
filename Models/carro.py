import tkinter as tk
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from base import Base
from cliente import Cliente
import enum

# Configuração do banco de dados
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class Status(enum.Enum):
    DISPONIVEL = "disponivel"
    ALUGADO = "alugado"
    EM_MANUNTENCAO = "em_manuntencao"
    FORA_DE_SERVICO = "fora_de_servico"

class Carro(Base):
    __tablename__ = 'automovel'
    placa = Column(String, primary_key=True)
    cor = Column(String)
    marca = Column(String)
    modelo = Column(String)
    valor = Column(Float)
    valor_diario = Column(Float)
    km = Column(Float)
    status = Column(Enum(Status))

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Funções para operações com carros
def adicionar_automovel_Interface():
    placa = entry_placa.get().strip()
    cor = entry_cor.get().strip()
    marca = entry_marca.get().strip()
    modelo = entry_modelo.get().strip()
    valor = entry_valor.get().strip()
    valor_diario = entry_valor_diario.get().strip()
    km = entry_km.get().strip()
    
    if not placa or not cor or not marca or not modelo or not valor or not valor_diario or not km:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return
    
    try:
        valor = float(valor)
        valor_diario = float(valor_diario)
        km = float(km)
    except ValueError:
        messagebox.showerror("Erro", "Insira valores numéricos válidos para valor, valor diário e km")
        return

    automovel_existente = session.query(Carro).filter_by(placa=placa).first()
    if automovel_existente:
        messagebox.showerror("Erro", f"Já existe um automóvel com a placa '{placa}'.")
        return

    novo_automovel = Carro(placa=placa, cor=cor, marca=marca, modelo=modelo, valor=valor, valor_diario=valor_diario, km=km, status=Status.DISPONIVEL)
    session.add(novo_automovel)
    session.commit()
    messagebox.showinfo("Sucesso", "Automóvel adicionado com sucesso.")
    limpar_campos()

def limpar_campos():
    entry_placa.delete(0, tk.END)
    entry_cor.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_valor_diario.delete(0, tk.END)
    entry_km.delete(0, tk.END)

def editar_automovel():
    placa = simpledialog.askstring("Editar Automóvel", "Digite a placa do automóvel a ser editado:")
    if not placa:
        return
    
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if not automovel:
        messagebox.showerror("Erro", f"Automóvel com placa '{placa}' não encontrado.")
        return

    nova_cor = simpledialog.askstring("Editar Automóvel", f"Nova cor (atual: {automovel.cor}):")
    novo_valor = simpledialog.askfloat("Editar Automóvel", f"Novo valor (atual: {automovel.valor}):")
    novo_valor_diario = simpledialog.askfloat("Editar Automóvel", f"Novo valor diário (atual: {automovel.valor_diario}):")
    nova_km = simpledialog.askfloat("Editar Automóvel", f"Nova quilometragem (atual: {automovel.km}):")
    
    automovel.cor = nova_cor if nova_cor else automovel.cor
    automovel.valor = novo_valor if novo_valor else automovel.valor
    automovel.valor_diario = novo_valor_diario if novo_valor_diario else automovel.valor_diario
    automovel.km = nova_km if nova_km else automovel.km
    session.commit()
    messagebox.showinfo("Sucesso", f"Automóvel '{placa}' atualizado com sucesso.")

def atualizar_status():
    placa = simpledialog.askstring("Atualizar Status", "Digite a placa do automóvel para atualizar o status:")
    if not placa:
        return
    
    automovel = session.query(Carro).filter_by(placa=placa).first()
    if not automovel:
        messagebox.showerror("Erro", f"Automóvel com placa '{placa}' não encontrado.")
        return

    status_selecionado = simpledialog.askstring("Atualizar Status", "Escolha o novo status (disponivel, alugado, em_manuntencao, fora_de_servico):")
    status_selecionado = status_selecionado.strip().lower()
    
    if status_selecionado not in [status.value for status in Status]:
        messagebox.showerror("Erro", "Status inválido.")
        return

    automovel.status = Status(status_selecionado)
    session.commit()
    messagebox.showinfo("Sucesso", f"Status do automóvel '{placa}' atualizado para '{status_selecionado}'.")

if __name__ == "__main__":
    # Criação da interface Tkinter
    root = tk.Tk()
    root.title("Gerenciamento de Automóveis")

    # Campos de entrada
    tk.Label(root, text="Placa:").grid(row=0, column=0)
    entry_placa = tk.Entry(root)
    entry_placa.grid(row=0, column=1)

    tk.Label(root, text="Cor:").grid(row=1, column=0)
    entry_cor = tk.Entry(root)
    entry_cor.grid(row=1, column=1)

    tk.Label(root, text="Marca:").grid(row=2, column=0)
    entry_marca = tk.Entry(root)
    entry_marca.grid(row=2, column=1)

    tk.Label(root, text="Modelo:").grid(row=3, column=0)
    entry_modelo = tk.Entry(root)
    entry_modelo.grid(row=3, column=1)

    tk.Label(root, text="Valor:").grid(row=4, column=0)
    entry_valor = tk.Entry(root)
    entry_valor.grid(row=4, column=1)

    tk.Label(root, text="Valor Diário:").grid(row=5, column=0)
    entry_valor_diario = tk.Entry(root)
    entry_valor_diario.grid(row=5, column=1)

    tk.Label(root, text="Quilometragem:").grid(row=6, column=0)
    entry_km = tk.Entry(root)
    entry_km.grid(row=6, column=1)

    # Botões
    btn_adicionar = tk.Button(root, text="Adicionar Automóvel", command=adicionar_automovel_Interface)
    btn_adicionar.grid(row=7, column=0, columnspan=2, pady=5)


    btn_status = tk.Button(root, text="Atualizar Status", command=atualizar_status)
    btn_status.grid(row=10, column=0, columnspan=2, pady=5)



    # Inicia o loop da interface
    root.mainloop()
