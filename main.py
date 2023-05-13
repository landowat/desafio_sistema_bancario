import textwrap

def menu():
    menu = """
    ================ MENU ================
    [d]  - Depositar
    [s]  - Sacar
    [e]  - Extrato
    [c]  - Cadastrar Conta Bancária
    [u]  - Cadastrar Usuário
    [cc] - Consultar Conta
    [uu] - Consultar Usuário
    [q]  - Sair

    => """
    return input(textwrap.dedent(menu))


def deposito_conta(saldo, extrato, /):
    try:
        valor_deposito = int(input("Valor do Depósito: "))
        if valor_deposito > 0:

            saldo += valor_deposito

            extrato += f"""Depósito R${valor_deposito}\n"""
            print(f"Seu saldo é de: R$ {saldo}")
        else:
            print("Valor inválido")

        return saldo, extrato
    except:
        print("Insira um valor válido")
        return saldo, extrato


def saque_conta(*, saldo, extrato, limite, limite_saques, numero_saques):
    try:
        valor_saque = int(input("Valor do Saque: "))
        if numero_saques >= limite_saques:
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

        return saldo, extrato, numero_saques
    except:
        print("Insira um valor válido")
        return saldo, extrato, numero_saques


def extrato_conta(saldo, /, extrato):

    print("------------------//--------------------")
    print("Extrato das últimas transações da conta:")
    print("------------------//--------------------")
    print(extrato)
    print("------------------//--------------------")
    print(f"Saldo da Conta: R$ {saldo}")
    print("------------------//--------------------")


def cadastrar_conta_bancaria(usuarios, numero_conta, AGENCIA):
    print("------------------//--------------------")
    print("Cadastrando nova Conta...")
    print("------------------//--------------------")
    cpf = input("CPF(sem caracteres): ")

    cpf_existe = verifica_cpf(usuarios, cpf)

    if cpf_existe:
        print("Conta criada com sucesso!!!")
        return {"cpf": cpf, "numero_conta": numero_conta, "agencia": AGENCIA}
    else:
        print(f"Usuário com CPF={cpf} não cadastrado!")
        return False


def cadastrar_usuario(usuarios):

    print("------------------//--------------------")
    print("Cadastrando novo Cliente...")
    print("------------------//--------------------")
    cpf = input("CPF(sem caracteres): ")

    cpf_repetido = verifica_cpf(usuarios, cpf)

    if cpf_repetido:
        print(f"Já existe usuário com CPF={cpf}!!!")
        return

    nome = input("Nome: ")
    data_nasc = input("Data de Nascimento: ")

    endereco = input("Endereço no seguinte formato: logradouro, nro - bairro - cidade/sigla estado")

    usuarios.append({"cpf": cpf, "nome": nome, "data_nasc": data_nasc, "endereco": endereco})

    print("Usuário cadastrado com sucesso!!!")
    print(f"Seja bem vindo, {nome}!")


def verifica_cpf(usuarios, cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True

    return False


def consultar_conta(contas):

    print("------------------//--------------------")
    print("Consultando contas...")
    print("------------------//--------------------")
    print(contas)


def consultar_usuario(usuarios):

    print("------------------//--------------------")
    print("Consultando Clientes...")
    print("------------------//--------------------")
    print(usuarios)


def main():

    # Constantes
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            saldo, extrato = deposito_conta(saldo, extrato)

        elif opcao == "s":
            saldo, extrato, numero_saques = saque_conta(saldo=saldo, extrato=extrato, limite=limite, limite_saques=LIMITE_SAQUES, numero_saques=numero_saques)

        elif opcao == "e":
            extrato_conta(saldo, extrato=extrato)

        elif opcao == "c":
            numero_conta = len(contas) + 1

            conta_criada = cadastrar_conta_bancaria(usuarios, numero_conta, AGENCIA)

            if conta_criada:
                contas.append(conta_criada)

        elif opcao == "u":
            cadastrar_usuario(usuarios)

        elif opcao == "cc":
            consultar_conta(contas)

        elif opcao == "uu":
            consultar_usuario(usuarios)

        elif opcao == "q":
            print("Volte sempre ao Banco Python")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()