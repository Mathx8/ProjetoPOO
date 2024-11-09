import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from base import Base
from carro import Carro, Status
from reserva import Reserva, StatusLocacao  
from cliente import Cliente
from sqlalchemy import DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, joinedload
from sqlalchemy.exc import NoResultFound
from pessoa import Locadora

engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

class Locacao(Base):
    __tablename__ = 'locacao'
    
    id = Column(Integer, primary_key=True)
    data_alocacao = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    data_devolucao = Column(DateTime)
    valor_total = Column(Integer)
    reserva_id = Column(Integer, ForeignKey('reservas.id'))
    carro_placa = Column(String, ForeignKey('automovel.placa'))
    cliente_id = Column(Integer, ForeignKey('cliente.id_cliente'))
    reserva = relationship('Reserva', back_populates='locacoes')
    carro = relationship('Carro', backref='locacoes')
    cliente = relationship('Cliente')

    @property
    def calcular_valor_total(self):
        if self.data_devolucao and self.data_alocacao:
            dias_alugados = (self.data_devolucao - self.data_alocacao).days
            if dias_alugados < 1:
                dias_alugados = 1

            valor_total_calculado = self.carro.valor + (dias_alugados * self.carro.valor_diario)
            print(f'Dias alugados: {dias_alugados}, Valor diário: {self.carro.valor_diario}, Valor total calculado: {valor_total_calculado}')
            return valor_total_calculado
        return 0

Base.metadata.create_all(engine)

def alugar_carro():
    cpf_cliente = simpledialog.askstring("Alugar Carro", "Digite o CPF do cliente:")
    carro_placa = simpledialog.askstring("Alugar Carro", "Digite a placa do carro:")
    
    try:
        carro = session.query(Carro).filter_by(placa=carro_placa).one()
        if carro.status != Status.DISPONIVEL:
            messagebox.showerror("Erro", "Carro não disponível para aluguel.")
            return
        
        cliente = session.query(Cliente).filter_by(Cpf=cpf_cliente).one_or_none()
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado. Por favor, registre o cliente primeiro.")
            return
        
        reserva = Reserva(status=StatusLocacao.RESERVADO)
        session.add(reserva)
        session.commit()

        locacao = Locacao(
            reserva_id=reserva.id,
            carro_placa=carro.placa,
            cliente_id=cliente.id_cliente
        )
        
        carro.status = Status.ALUGADO
        session.add(locacao)
        session.commit()

        messagebox.showinfo("Sucesso", f"Carro {carro.placa} alugado com sucesso para o cliente {cliente.Nome}.")

    except NoResultFound:
        messagebox.showinfo("Erro", "Carro ou reserva não encontrada.")
        session.rollback()
    except Exception as e:
        messagebox.showinfo("Erro", f"Ocorreu um erro: {e}")
        session.rollback()
        
def devolver_carro():
    cpf_cliente = simpledialog.askstring("Devolver Carro", "Digite o cpf do cliente: ")
    carro_placa = simpledialog.askstring("Devolver Carro", "Digite a placa do carro alugado: ")
    try:
        cliente = session.query(Cliente).filter_by(Cpf=cpf_cliente).one_or_none()
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return
        
        locacao = session.query(Locacao).filter_by(cliente_id=cliente.id_cliente, carro_placa=carro_placa).all()
        if not locacao:
            messagebox.showerror("Erro", "Locação não encontrada para este cliente e carro.")
            return
        
        locacao = max(locacao, key=lambda l: l.data_alocacao)
        
        carro = session.query(Carro).filter_by(placa=carro_placa).one_or_none()
        if not carro:
            messagebox.showerror("Erro", "Carro não encontrado.")
            return
        
        reserva = session.query(Reserva).filter_by(id=locacao.reserva_id).one_or_none()
        if reserva:
            reserva.status = StatusLocacao.DEVOLVIDO

        carro.status = Status.DISPONIVEL
        locacao.data_devolucao = datetime.datetime.now(datetime.timezone.utc)
        
        session.commit()

        locacao.valor_total = locacao.calcular_valor_total
        session.commit()
        
        messagebox.showinfo("Sucesso", f"Carro {carro.placa} devolvido com sucesso pelo cliente {cliente.Nome}. Valor total a pagar: R$ {locacao.valor_total:.2f}")
    
    except NoResultFound:
        messagebox.showerror("Erro", "Erro ao localizar carro ou locação.")
        session.rollback()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        session.rollback()

def ver_reservas():
    reservas = session.query(Locacao).options(joinedload(Locacao.carro), joinedload(Locacao.cliente)).all()

    if not reservas:
        messagebox.showinfo("Reservas", "Nenhuma reserva encontrada.")
        return

    consulta_texto = ""
    for reserva in reservas:
        valor_total_texto = f"R$ {reserva.valor_total:.2f}" if reserva.valor_total is not None else "Em andamento"

        consulta_texto += (
            f"Reserva ID: {reserva.id}\n"
            f"Cliente: {reserva.cliente.Nome}\n"
            f"Carro: {reserva.carro.modelo}\n"
            f"Placa: {reserva.carro.placa}\n"
            f"Data de Alocação: {reserva.data_alocacao}\n"
            f"Data de Devolução: {reserva.data_devolucao or 'Ainda não devolvido'}\n"
            f"Valor Total: {valor_total_texto}\n{'-'*50}\n"
        )

    messagebox.showinfo("Reservas de Automóveis", consulta_texto)

root = tk.Tk()
root.title("Sistema de Locação de Automóveis")

btn_alugar_carro = tk.Button(root, text="Alugar Automóvel", command=alugar_carro)
btn_alugar_carro.grid(row=0, column=0, padx=10, pady=5)

btn_devolver_carro = tk.Button(root, text="Devolver Automóvel", command=devolver_carro)
btn_devolver_carro.grid(row=1, column=0, padx=10, pady=5)

btn_ver_reservas = tk.Button(root, text="Ver Reservas", command=ver_reservas)
btn_ver_reservas.grid(row=2, column=0, padx=10, pady=5)

root.mainloop()
