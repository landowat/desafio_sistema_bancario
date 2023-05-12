menu = """

[d] - Depositar
[s] - Sacar
[e] - Extrato
[q] - Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        try:
            valor_deposito = int(input("Valor do Depósito: "))
            if valor_deposito > 0:
                saldo += valor_deposito
                extrato += f"""Depósito R${valor_deposito}\n"""
                print(f"Seu saldo é de: R$ {saldo}")
            else:
                print("Valor inválido")
        except:
            print("Insira um valor válido")
            continue


    elif opcao == "s":
        try:
            valor_saque = int(input("Valor do Saque(limite de R$ 500): "))
            if numero_saques >= LIMITE_SAQUES:
                print("Você atingiu o limite de 3 saques diários.")
            elif valor_saque > limite:
                print("Você tentou sacar valor acima do limite(R$ 500).")
            else:
                if valor_saque > 0:
                    if saldo >= valor_saque:
                        saldo -= valor_saque
                        numero_saques += 1
                        extrato += f"""Saque R${valor_saque}\n"""
                        print(f"Seu saldo é de: R$ {saldo}")
                    else:
                        print("Saldo insuficiente para efetuar saque.")
                else:
                    print("Não é possível sacar valor negativo.")
        except:
            print("Insira um valor válido")
            continue

    elif opcao == "e":
        print("------------------//--------------------")
        print("Extrato das últimas transações da conta:")
        print("------------------//--------------------")
        print(extrato)
        print("------------------//--------------------")
        print(f"Saldo da Conta: R$ {saldo}")
        print("------------------//--------------------")

    elif opcao == "q":
        print("Volte sempre ao Banco Python")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
