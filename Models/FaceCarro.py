import tkinter as tk
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine, Column, Float, Enum, String
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

# Funções para operações com carros
def adicionar_automovel():
    try:
        placa = entry_placa.get().strip()
        cor = entry_cor.get().strip()
        marca = entry_marca.get().strip()
        modelo = entry_modelo.get().strip()
        valor = float(entry_valor.get().strip())
        valor_diario = float(entry_valor_diario.get().strip())
        km = float(entry_km.get().strip())
        
        if not all([placa, cor, marca, modelo]):
            raise ValueError("Preencha todos os campos obrigatórios.")

        automovel_existente = session.query(Carro).filter_by(placa=placa).first()
        if automovel_existente:
            messagebox.showerror("Erro", f"Já existe um automóvel com a placa '{placa}'.")
            return

        novo_automovel = Carro(placa=placa, cor=cor, marca=marca, modelo=modelo, valor=valor, valor_diario=valor_diario, km=km, status=Status.DISPONIVEL)
        session.add(novo_automovel)
        session.commit()
        messagebox.showinfo("Sucesso", "Automóvel adicionado com sucesso.")
        limpar_campos()
        
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

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
    automovel.valor = novo_valor if novo_valor is not None else automovel.valor
    automovel.valor_diario = novo_valor_diario if novo_valor_diario is not None else automovel.valor_diario
    automovel.km = nova_km if nova_km is not None else automovel.km
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
    btn_adicionar = tk.Button(root, text="Adicionar Automóvel", command=adicionar_automovel)
    btn_adicionar.grid(row=7, column=0, columnspan=2, pady=5)

    btn_editar = tk.Button(root, text="Editar Automóvel", command=editar_automovel)
    btn_editar.grid(row=8, column=0, columnspan=2, pady=5)

    btn_status = tk.Button(root, text="Atualizar Status", command=atualizar_status)
    btn_status.grid(row=9, column=0, columnspan=2, pady=5)

    # Inicia o loop da interface
    root.mainloop()
