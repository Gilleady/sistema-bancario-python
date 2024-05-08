from abc import ABC, abstractmethod
from datetime import datetime
import functools
import textwrap


class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._contador]            
            lista_contas = str(conta) + "|" + f"Saldo: R$ {conta.saldo:.2f}".center(98) + "|\n"
            
            return lista_contas
        except IndexError:
            raise StopIteration
        finally:
            self._contador += 1


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
        linha = "+" + "-" * 98 + "+\n"
        linha += "|" + f"Agência: {self.agencia}".center(98) + "|\n"
        linha += "|" + f"C/C: {self.numero}".center(98) + "|\n"
        linha += "|" + f"Titular: {self.cliente.nome}".center(98) + "|\n"
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
                "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


    def gerar_relatorio(self, tipo_transacao="todos"):
        for transacao in self.transacoes:
            if tipo_transacao.lower() == "todos" or transacao["tipo"].lower() == tipo_transacao.lower():
                    yield transacao


    def transacoes_do_dia(self):
        qtd_transacoes = 0
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S")
            
            if data_transacao.date() == datetime.utcnow().date():
                qtd_transacoes += 1
        
        return qtd_transacoes


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
        qtd_transacoes_dia = conta.historico.transacoes_do_dia()
        if qtd_transacoes_dia >= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return
        
        transacao.registrar(conta)


    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


def log_transacao(func):
    @functools.wraps(func)
    def log(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"LOGS: {func.__name__} - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")
        return resultado

    return log


def menu():
    menu = "+" + "-" * 40 + " SISTEMA BANCÁRIO " + "-" * 40 + "+\n"
    menu += "|" + " [d] Depositar  ".center(98) + "|\n"
    menu += "|" + "[s] Sacar    ".center(98) + "|\n"
    menu += "|" + " [e] Extrato   ".center(98) + "|\n"
    menu += "|" + "   [u] Novo Cliente".center(98) + "|\n"
    menu += "|" + " [c] Nova Conta".center(98) + "|\n"
    menu += "|" + "    [l] Listar Contas".center(98) + "|\n"
    menu += "|" + "[q] Sair     ".center(98) + "|\n"
    menu += "+" + "-" * 98 + "+\n"
    menu += "=>"

    return input(textwrap.dedent(menu))


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


@log_transacao
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


@log_transacao
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


@log_transacao
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

    tipo_transacao = input("Digite qual tipo de transação para exibir no extrato ('Saque', 'Deposito' ou 'Todos'): ")

    for transacao in conta.historico.gerar_relatorio(tipo_transacao):
        extrato += "|" + f"{transacao["data"]} - {transacao["tipo"]}: R$ {transacao["valor"]:.2f}".center(98) + "|\n"
    
    print("+" + "-" * 45 + " EXTRATO " + "-" * 44 + "+")
    print("| Não foram realizadas movimentações | " if not extrato else extrato.rstrip())
    print("|" + f"Saldo da conta: R$ {conta.saldo:.2f}".center(98) + "|")
    print("+" + "-" * 98 + "+")


@log_transacao
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


@log_transacao
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
    listagem = ""
    for info_conta in ContaIterador(contas):
        listagem += str(info_conta)
        
    print(listagem + "+" + "-" * 98 + "+\n" if listagem else "Nenhuma conta para listar")


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