import textwrap


def menu():
    menu = """ 
    +--------- SISTEMA BANCÁRIO ---------+
    |           [d] Depositar            |
    |           [s] Sacar                |
    |           [e] Extrato              |
    |           [q] Sair                 |
    +------------------------------------+
    =>"""
    return input(textwrap.dedent(menu))

def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saques = numero_saques >= limite_saques
    excedeu_limite = valor > limite
    excedeu_saldo = valor > saldo

    if excedeu_saques:
        status_operacao = "Operação falhou! Número máximo de saques excedido."

    elif excedeu_limite:
        status_operacao = "Operação falhou! O valor do saque excede o limite."

    elif excedeu_saldo:
        status_operacao = "Operação falhou! Você não tem saldo suficiente."

    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += "|" + f"Saque: R$ {valor:.2f}".center(36) + "|\n"
        status_operacao = "Saque efetuado com sucesso! Verifique o extrato para mais informações."

    else:
        status_operacao ="Operação falhou! Valor informado é inválido."
    
    print(status_operacao)

    return saldo, extrato, numero_saques

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:

        opcao = menu()

        if opcao == "d":
            deposito = float(input("Insira um valor para depósito: "))

            if deposito > 0:
                saldo += deposito
                extrato += "|" + f"Depósito: R$ {deposito:.2f}".center(36) + "|\n"
                print("Deposito feito com sucesso")

            else:
                print("Valor inválido para depósito. Tente novamente!")

        elif opcao == "s":
            valor = float(input("Insira um valor que deseja sacar: "))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            print("+------------- EXTRATO --------------+")
            print("| Não foram realizadas movimentações | " if not extrato else extrato.rstrip())
            print("|"+f"Saldo da conta: R$ {saldo:.2f}".center(36)+"|")
            print("+------------------------------------+")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()