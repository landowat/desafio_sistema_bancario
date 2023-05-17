import textwrap
from abc import abstractmethod, ABC
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        print("Realizando transacao...")
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def consulta_dados(self):
        lista_contas = []

        cpf_formatado = '{}.{}.{}-{}'.format(self.cpf[:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:])
        data_formatada = '{}/{}/{}' \
            .format(self.data_nascimento[:2], self.data_nascimento[2:4], self.data_nascimento[4:8])

        for conta in self.contas:
            lista_contas.append(conta.numero)

        print(f"Cliente: {self.nome}, "
              f"CPF: {cpf_formatado}, "
              f"Data Nasc: {data_formatada}, "
              f"Contas: {lista_contas}")


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
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.saldo
        #excedeu_saldo = valor > saldo

        if valor > saldo:
            print("Saldo insuficiente para efetuar saque.")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            print(f"Saldo atual: {self.saldo}")
            return True
        else:
            print("Ocorreu um erro inesperado!!!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            print(f"Saldo atual: {self.saldo}")
            return True
        else:
            print("Valor inválido")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = 500
        self._limite_saques = 3

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__]
        )

        if valor > self._limite:
            print("Você tentou sacar valor acima do limite(R$ 500).")

        elif numero_saques >= self._limite_saques:
            print("Você atingiu o limite de 3 saques diários.")

        else:
            return super().sacar(valor)

        return False

    def consulta_dados(self):
        print(f"Conta: {self.numero}, "
              f"Cliente: {self.cliente.nome}, "
              f"Agencia: {self.agencia}")


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Transacao": transacao.valor,
                "Timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
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
        print("Registrando transacao...")
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
        print(f"Conta registrada: {conta}")
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


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


def deposito_conta(clientes):

    cpf = input("CPF(sem caracteres): ")

    cliente = verifica_cpf(clientes, cpf)

    if not cliente:
        print(f"Usuário com CPF={cpf} não cadastrado!")
        return False

    conta = define_conta_cliente(cliente)

    if not conta:
        print("Conta não encontrada. Digite uma conta válida!")
        return

    try:
        valor_deposito = float(input("Valor do Deposito: "))
    except:
        print("Insira um valor válido")
        return

    transacao = Deposito(valor_deposito)

    cliente.realizar_transacao(conta, transacao)


def saque_conta(clientes):

    cpf = input("CPF(sem caracteres): ")

    cliente = verifica_cpf(clientes, cpf)

    if not cliente:
        print(f"Usuário com CPF={cpf} não cadastrado!")
        return False

    conta = define_conta_cliente(cliente)

    if not conta:
        print("Conta não encontrada. Digite uma conta válida!")
        return

    try:
        valor_saque = float(input("Valor do Saque: "))
    except:
        print("Insira um valor válido")
        return

    transacao = Saque(valor_saque)

    cliente.realizar_transacao(conta, transacao)


def extrato_conta(clientes):

    cpf = input("CPF(sem caracteres): ")

    cliente = verifica_cpf(clientes, cpf)

    if not cliente:
        print(f"Usuário com CPF={cpf} não cadastrado!")
        return False

    conta = define_conta_cliente(cliente)

    if not conta:
        print("Conta não encontrada. Digite uma conta válida!")
        return

    print("--------------------------------//--------------------------------")
    print("Extrato das últimas transações da conta:")
    print("--------------------------------//--------------------------------")

    for transacao in conta.historico.transacoes:
        print('{:>8}: {:>15} {:>40}'.format(transacao['Tipo'], transacao['Transacao'], transacao['Timestamp']))

    print(f"")
    print("--------------------------------//--------------------------------")
    print(f"            Saldo da Conta: R$ {conta.saldo}")
    print("--------------------------------//--------------------------------")


def cadastrar_conta_bancaria(clientes, numero_conta, contas):
    print("------------------//--------------------")
    print("Cadastrando nova Conta...")
    print("------------------//--------------------")
    cpf = input("CPF(sem caracteres): ")

    cliente = verifica_cpf(clientes, cpf)

    if cliente:
        conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)
        contas.append(conta)
        # cliente.contas.append(conta)
        cliente.adicionar_conta(conta)

        print("Conta criada com sucesso!!!")
    else:
        print(f"Usuário com CPF={cpf} não cadastrado!")
        return False


def cadastrar_cliente(clientes):
    print("------------------//--------------------")
    print("Cadastrando novo Cliente...")
    print("------------------//--------------------")
    cpf = input("CPF(sem caracteres): ")

    cliente = verifica_cpf(clientes, cpf)

    if cliente:
        print(f"Já existe usuário com CPF={cpf}!!!")
        return

    nome = input("Nome: ")
    data_nasc = input("Data de Nascimento: ")

    endereco = input("Endereço no seguinte formato: logradouro, nro - bairro - cidade/sigla estado")

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nasc, endereco=endereco)

    clientes.append(cliente)

    print("Usuário cadastrado com sucesso!!!")
    print(f"Seja bem vindo, {nome}!")


def verifica_cpf(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente

    return False


def consultar_conta(contas):
    print("--------------------------------//--------------------------------")
    print("                      Consultando Contas")
    print("--------------------------------//--------------------------------")
    for conta in contas:
        conta.consulta_dados()


def consultar_usuario(clientes):
    print("--------------------------------//--------------------------------")
    print("                      Consultando Clientes")
    print("--------------------------------//--------------------------------")
    for cliente in clientes:
        cliente.consulta_dados()


def define_conta_cliente(cliente):
    lista_contas = []

    if not cliente.contas:
        print("Cliente não possui conta cadastrada")
        return

    print(f"Lista com as contas do cliente {cliente.nome}:")
    for conta in cliente.contas:
        lista_contas.append(conta.numero)
        print(f"{conta.numero}")

    numero_conta = int(input("Digite o número da conta: "))

    for linha in range(len(lista_contas)):
        # print(f"index: {lista_contas[linha]}")
        if numero_conta == lista_contas[linha]:
            return cliente.contas[linha]

    print(f"Numero de conta não cadastrada!!!")

    return None



def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            deposito_conta(clientes)

        elif opcao == "s":
            saque_conta(clientes)

        elif opcao == "e":
            extrato_conta(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            conta_criada = cadastrar_conta_bancaria(clientes, numero_conta, contas)

        elif opcao == "u":
            cadastrar_cliente(clientes)

        elif opcao == "cc":
            consultar_conta(contas)

        elif opcao == "uu":
            consultar_usuario(clientes)

        elif opcao == "q":
            print("Volte sempre ao Banco Python")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
