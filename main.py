menu = """ 
        +- Sistema Bancário -+
        | [d] Depositar      |
        | [s] Sacar          |
        | [e] Extrato        |
        | [q] Sair           |
        +--------------------+
=>"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        deposito = float(input("Insira um valor para depósito: "))

        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"
            print("Deposito feito com sucesso")

        else:
            print("Valor inválido para depósito. Tente novamente!")

    elif opcao == "s":
        saque = float(input("Insira um valor que deseja sacar: "))
        if (numero_saques < LIMITE_SAQUES) and (saque <= limite) and (saque <= saldo):
            saldo -= saque
            numero_saques += 1
            extrato += f"Saque: R$ {saque:.2f}\n"
            print("Saque efetuado com sucesso! Verifique o extrato para mais informações.")
        else:
            print("Não foi possível sacar o dinheiro. Saldo insuficiente ou limite de saques atingido.")

    elif opcao == "e":
        print(extrato)
        print(f"Saldo da conta: R$ {saldo:.2f}")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
