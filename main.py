from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()


    @property
    def saldo(self):
        return self._saldo


    @property
    def numero(self):
        return self._numero


    @property
    def agencia(self):
        return self._agencia


    @property
    def cliente(self):
        return self._cliente


    @property
    def historico(self):
        return self._historico


    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)


    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    
    def __str__(self) -> str:
        linha = "+" + "-" * 36 + "+\n"
        linha += "|" + f"Agência: {self.agencia}".center(36) + "|\n"
        linha += "|" + f"C/C: {self.numero}".center(36) + "|\n"
        linha += "|" + f"Titular: {self.cliente.nome}".center(36) + "|\n"
        return linha


class Historico:
    def __init__(self):
        self._transacoes = []


    @property
    def transacoes(self):
        return self._transacoes


    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass


    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor


    @property
    def valor(self):
        return self._valor


    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor


    @property
    def valor(self):
        return self._valor


    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []


    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


def menu():
    menu = """ 
    +--------- SISTEMA BANCÁRIO ---------+
    |           [d] Depositar            |
    |           [s] Sacar                |
    |           [e] Extrato              |
    |           [u] Novo Cliente         |
    |           [c] Nova Conta           |
    |           [l] Listar Contas        |
    |           [q] Sair                 |
    +------------------------------------+
    =>"""
    return input(textwrap.dedent(menu))


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, operação de depósito cancelada!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, operação de saque cancelada!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, operação de saque cancelada!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    extrato = ""

    for transacao in conta.historico.transacoes:
        extrato = "|" + f"{transacao.data} - {transacao.tipo}: R$ {transacao.valor:.2f}".center(36) + "|\n"
    
    print("+------------- EXTRATO --------------+")
    print("| Não foram realizadas movimentações | " if not extrato else extrato.rstrip())
    print("|"+f"Saldo da conta: R$ {conta.saldo:.2f}".center(36)+"|")
    print("+------------------------------------+")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números):")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nCliente já cadastrado com CPF informado!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (Logradouro, nº - Bairro - Cidade/UF): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Cliente criado com sucesso!")


def filtrar_cliente(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None


def criar_conta(numero_conta, contas, clientes):
    cpf = input("Informe o CPF do Cliente (somente números):")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, operação de criação de conta cancelada!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")


def listar_contas(contas):
    lista_contas = ""
    for conta in contas:
        lista_contas += str(conta)
        
    print(lista_contas + "+" + "-" * 36 + "+\n" if lista_contas else "Nenhuma conta para listar")


def main():
    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, contas, clientes)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()