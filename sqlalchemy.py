import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import select
from sqlalchemy import func

Base = declarative_base()
engine = create_engine("sqlite://")

class Cliente(Base):

    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9), unique=True)
    endereco = Column(String, unique=True)

    conta = relationship("Conta", back_populates='cliente')

    def __repr__(self):
        return f"Cliente(id={self.id}, nome = {self.nome}, cpf = {self.cpf}, endereco = {self.endereco})"

class Conta(Base):

    __tablename__ = "conta"

    id = Column(Integer,primary_key=True)
    tipo = Column(String,nullable=False)
    agencia = Column(String,nullable=False)
    numero = Column(String,unique=True,nullable=False)
    saldo = Column(Integer)
    cliente_id = Column(Integer,ForeignKey('cliente.id'), nullable=False)
    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo = {self.tipo}, agencia = {self.agencia}, numero = {self.numero})"
    
Base.metadata.create_all(engine)

with Session(engine) as session:
    Caio = Cliente(nome="caio toys", cpf="123456789", endereco="maringá-pr", conta=[Conta(tipo="conta corrente", agencia="0001", numero="1",saldo=30)])
    Arthur = Cliente(nome="arthur crimeia", cpf="023456789", endereco="sarandi-pr", conta=[Conta(tipo="conta corrente", agencia="0001", numero="2",saldo=31),
        Conta(tipo = "conta corrente", agencia="0002", numero = "4", saldo=32)                                                                               
    ])
    Joaquim = Cliente(nome="joaquim silva", cpf = "082341879", endereco="curitiba-pr", conta=[Conta(tipo="conta corrente", agencia="0001", numero="8", saldo=90)])

    session.add_all([Caio,Arthur,Joaquim])
    session.commit()

print("---------------------------------------------------------------------------\n")
print("Exibindo instancias dos clientes:\n")
stmt = select(Cliente).where(Cliente.nome.in_(['caio toys','arthur crimeia','joaquim silva']))
for cliente in session.scalars(stmt):
    print(cliente)
print("---------------------------------------------------------------------------\n")

print("Exibindo instancias das contas de Arthur:")
stmt_conta = select(Conta).where(Conta.cliente_id.in_([2]))
for conta in session.scalars(stmt_conta):
    print(conta)
print("---------------------------------------------------------------------------\n")

print("Exibindo de maneira ordenada:")
stmt_order = select(Conta).order_by(Conta.saldo.desc())
for saldo_conta in session.scalars(stmt_order):
    print(saldo_conta)
print("---------------------------------------------------------------------------\n")

print("Exibindo total de instancias dentro da classe cliente:")
stmt_count = select(func.count('*')).select_from(Cliente)
for numero_instancias in session.scalars(stmt_count):
    print(numero_instancias)
print("---------------------------------------------------------------------------\n")



