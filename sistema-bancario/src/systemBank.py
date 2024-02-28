import random
import textwrap

# Implementar 3 operações: depósito, saque e extrato.
# Criar duas ovas funções: cadastrar usuário (cliente) e cadastrar conta bancária
# Criar funções para as operações existentes: sacar, depositar e visualizar histórico


def menu():
    menu = """\n
    ============ MENU ============
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo usuário
    [5]\tNova conta
    [6]\tListar contas
    [7]\tSair\n
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print("\nDeposíto realizado com sucesso!")
    else:
        print("\nOperação invalida")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_de_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_de_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou ! Saldo insuficiente. ")
    elif excedeu_limite:
        print("\nOperação falhou ! O valor ultrapassa o limite de saque.")
    elif excedeu_saques:
        print("\nOperação falhou ! Número máximo de saques excedido. ")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \tR$ {valor:.2f}\n"
        numero_de_saques += 1
        print("\n Saque realizado com sucesso! ")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n Extrato ")
    print("Não realizou movimentações. " if not extrato else extrato)
    print(f"\nSaldo: \tR$ {saldo:.2f}")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )
    usuarios.append(
        {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }
    )
    print("\n Usuário criado com sucesso! ")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nConta criada com sucesso ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n Usuario não encontrado !")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))


def main():
    LIMITES_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_de_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "1":
            valor = float(input("Informe o valor do deposito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_de_saques=numero_de_saques,
                limite_saques=LIMITES_SAQUES,
            )
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "4":
            criar_usuario(usuarios)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            break
        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


main()
