# Implementar 3 operações: depósito, saque e extrato.
"""
  Operação de depósito

  Deve ser possível depositar valores positivos para a minha conta bancária. A v1 do projto
  trabalha apenas com 1 usuário, dessa forma não precisamos nos preocupar em identificar
  qual é o número da agência e conta bancária. Todos os depósitos devem ser armazenados
  em uma variável e exibidos na operação de extrato.
  
"""
"""
  Operação de saque

  O sistema deve permitir realizar 3 saques diários com limite máximo de R$ 500,00 por saque.
  Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mensagem informando que
  não será possível sacar o dinheiro por falta de saldo. Todos os saques devem ser armazenados
  em uma variável e exibidos na operação de extrato
  
"""
"""
  Operação de extrato

  Deve listar todos os depósitos e saques realizados na conta. No fim da listagem deve ser
  exibido o saldo atual da conta. Os valores devem ser exibidos utilizando o forma R$ xxx.xx.
  
"""
# Definindo um saldo aleatório a conta
saldo_da_conta = 500
qtd_saques = 0
extrato = {"Deposito": [], "Saque": []}


def menu():
    print(
        """
      Operações Sistema Bancário

      [Saque] - Operação de Saque
      [Deposito] - Operação de Deposito
      [Extrato] - Operação de Extrato

      [Sair] - Operação de saida

      Digite a operação desejada: 
    """
    )


def systemBank():
    global saldo_da_conta, qtd_saques, extrato
    while True:
        menu()
        opcao = input()
        if opcao == "Saque":
            if qtd_saques < 3:
                limite_saque = 500
                valor_saque = float(input("Digite o valor a ser sacado: "))
                if valor_saque > saldo_da_conta:
                    print("Não é possível realizar essa operação! Saldo Indisponivel")
                elif valor_saque > limite_saque:
                    print("Limite Ultrapassado !")
                elif valor_saque <= limite_saque:
                    saldo_da_conta -= valor_saque
                    extrato["Saque"].append(valor_saque)
                    print("Saque realizado com sucesso !")
                    qtd_saques += 1
            else:
                print("Você atingiu o limite de saque diário !")
        elif opcao == "Deposito":
            valor_deposito = float(input("Digite o valor a ser depósitado: "))
            if valor_deposito < 0:
                print("Não é possível depositar valores negativos")
            else:
                saldo_da_conta += valor_deposito
                extrato["Deposito"].append(valor_deposito)
                print("Depósito realizado com sucesso !")
        elif opcao == "Extrato":
            print(f"Depósitos realizados\n{extrato['Deposito']}")
            print(f"Saques realizados\n{extrato['Saque']}")
            print(f"Saldo final da conta: {saldo_da_conta:.2f}")
            pass
        elif opcao == "Sair":
            print("Saindo do Sistema !")
            return False
        else:
            print("Opção invalida ! Digite novamente !")


systemBank()
