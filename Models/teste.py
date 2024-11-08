import tkinter as tk
from tkinter import messagebox,simpledialog
from sqlalchemy import create_engine, Column, String, Float, Enum
from sqlalchemy.orm import sessionmaker
from base import Base
from Erros import PlacaExistenteException, InvalidaException  # Assumindo que você tem essas exceções
import enum

# Configuração do banco de dados
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class Status(enum.Enum):
    DISPONIVEL = "disponivel"
    ALUGADO = "alugado"
    EM_MANUTENCAO = "em manutencao"
    FORA_DE_SERVICO = "fora de servico"

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

    def __init__(self, placa, cor, marca, modelo, valor, valor_diario, km):
        self.placa=placa
        self.cor=cor
        self.marca=marca
        self.modelo=modelo
        self.valor=valor
        self.valor_diario=valor_diario
        self.km=km
        self.status = Status.DISPONIVEL

    def Validar_placa(self, placa):
        if not placa or len(placa) < 7:
            raise ValueError("Placa inválida. Deve conter 7 caracteres.")
        if session.query(Carro).filter_by(placa=placa).first():
            raise PlacaExistenteException
        self.placa = placa

    def Validar_cor(self, cor):
        if not cor:
            raise ValueError("A cor não pode ser vazia.")
        self.cor = cor

    def Validar_marca(self, marca):
        if not marca:
            raise ValueError("A marca não pode ser vazia.")
        self.marca = marca

    def Validar_modelo(self, modelo):
        if not modelo:
            raise ValueError("O modelo não pode ser vazio.")
        self.modelo = modelo

    def Validar_valor(self, valor):
        try:
            valor = float(valor)
            if valor < 0:
                raise InvalidaException
            self.valor = valor
        except ValueError:
            raise InvalidaException


    def Validar_valor_diario(self, valor_diario):
        try:
            valor_diario = float(valor_diario)
            if valor_diario < 0:
                raise InvalidaException
            self.valor_diario = valor_diario
        except ValueError:
            raise InvalidaException
        
    def Validar_km(self, km):
        try:
            km = float(km)
            if km < 0:
                raise InvalidaException
            self.km = km
        except ValueError:
            raise InvalidaException
            
    def Validar_status(self, status):
        if status not in Status.__members__:
            raise ValueError("Status inválido. Escolha um dos seguintes: disponível, alugado, em manutenção, fora de serviço.")
        self.status = Status[status]

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
    
    novo_status = simpledialog.askstring("Atualizar Status", "Escolha um dos seguintes: disponível, alugado, em manutencao, fora de servico.")
    novo_status = novo_status.strip().lower()
    
    automovel.status = Status(novo_status)
    session.commit()
    messagebox.showinfo("Sucesso", f"Status do automóvel '{placa}' atualizado para '{novo_status}'.")


    
# Função para adicionar automóvel pela interface
def adicionar_automovel_interface():
    placa = entry_placa.get()
    cor = entry_cor.get()
    marca = entry_marca.get()
    modelo = entry_modelo.get()
    valor = entry_valor.get()
    valor_diario = entry_valor_diario.get()
    km = entry_km.get()
    

    try:

        novo_carro = Carro(placa, cor, marca, modelo, valor, valor_diario, km)

        novo_carro.Validar_placa(placa)
        novo_carro.Validar_cor(cor)
        novo_carro.Validar_marca(marca)
        novo_carro.Validar_modelo(modelo)
        novo_carro.Validar_valor(valor)
        novo_carro.Validar_valor_diario(valor_diario)
        novo_carro.Validar_km(km)
        
        session.add(novo_carro)
        session.commit()
        messagebox.showinfo("Sucesso", "Automóvel adicionado com sucesso.")
        
        
        entry_placa.delete(0, tk.END)
        entry_cor.delete(0, tk.END)
        entry_marca.delete(0, tk.END)
        entry_modelo.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
        entry_valor_diario.delete(0, tk.END)
        entry_km.delete(0, tk.END)

    except PlacaExistenteException as e:
        messagebox.showerror("Erro de Placa", str(e))
    except InvalidaException as e:
        messagebox.showerror("Erro de Valor",str(e) )
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro Desconhecido", str(e))

# Função para limpar os campos de entrada



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
btn_adicionar = tk.Button(root, text="Adicionar Automóvel", command=adicionar_automovel_interface)
btn_adicionar.grid(row=7, column=0, columnspan=2, pady=5)

btn_consultar = tk.Button(root, text="Consultar Automóveis", command=consultar_automovel)
btn_consultar.grid(row=8, column=0, columnspan=2, pady=5)

btn_status = tk.Button(root, text="Atualizar Status", command=atualizar_status)
btn_status.grid(row=9, column=0, columnspan=2, pady=5)

btn_status = tk.Button(root, text="Editar Automavel", command=editar_automovel)
btn_status.grid(row=10, column=0, columnspan=2, pady=5)

# Inicia o loop da interface
root.mainloop()
