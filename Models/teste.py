import tkinter as tk
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine, Column, Integer, String, Float, Enum
from sqlalchemy.orm import sessionmaker
from base import Base
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

# Função para adicionar automóvel
def adicionar_automovel():
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

# Função para consultar automóveis
def consultar_automovel():
    automoveis = session.query(Carro).all()

    if not automoveis:
        messagebox.showinfo("Consulta", "Nenhum automóvel encontrado.")
        return

    consulta_texto = ""
    for automovel in automoveis:
        consulta_texto += (
            f"Placa: {automovel.placa}\n"
            f"Cor: {automovel.cor}\n"
            f"Marca: {automovel.marca}\n"
            f"Modelo: {automovel.modelo}\n"
            f"Valor: {automovel.valor}\n"
            f"Valor diário: {automovel.valor_diario}\n"
            f"Quilometragem: {automovel.km}\n"
            f"Status: {automovel.status.value}\n{'-'*20}\n"
        )

    messagebox.showinfo("Consulta de Automóveis", consulta_texto)

# Função para limpar os campos de entrada
def limpar_campos():
    entry_placa.delete(0, tk.END)
    entry_cor.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_valor_diario.delete(0, tk.END)
    entry_km.delete(0, tk.END)

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
btn_adicionar = tk.Button(root, text="Adicionar Automóvel", command=adicionar_automovel)
btn_adicionar.grid(row=7, column=0, columnspan=2, pady=5)

btn_consultar = tk.Button(root, text="Consultar Automóveis", command=consultar_automovel)
btn_consultar.grid(row=8, column=0, columnspan=2, pady=5)

# Inicia o loop da interface
root.mainloop()
