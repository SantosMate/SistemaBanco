from abc import ABC, abstractmethod
from datetime import date

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("Saldo insuficiente!")
        else:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")

class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def mostrar_extrato(self):
        print("\n===== EXTRATO =====")
        if not self.transacoes:
            print("Nenhuma transação realizada.")
        else:
            for t in self.transacoes:
                print(t)

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        cliente.adicionar_conta(self)

    def sacar(self, valor):
        transacao = Saque(valor)
        transacao.registrar(self)

    def depositar(self, valor):
        transacao = Deposito(valor)
        transacao.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Simulação de uso
cliente = PessoaFisica("12345678900", "João Silva", date(1990, 5, 15), "Rua A, 123")
conta = ContaCorrente(cliente, "1001")

conta.depositar(1000)
conta.sacar(300)
conta.historico.mostrar_extrato()
