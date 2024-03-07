import textwrap
from abc import ABC, abstractclassmethod, abstractproperty


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._agency = "0001"
        self._number = number
        self._client = client
        self._historic = Historic()

    @property
    def balance(self):
        return self._balance

    @property
    def agency(self):
        return self._agency

    @property
    def number(self):
        return self._number

    @property
    def client(self):
        return self.client

    @property
    def historic(self):
        return self._historic

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    def draw(self, value):
        balance = self._balance
        exceed_limit = value > balance
        if exceed_limit:
            print("\n==== Operation Failed ! Insufficient balance ====\n")
        elif value > 0:
            self._balance -= value
            print("\n==== Valid Operation ! Successful draw \n")
            return True
        else:
            print("\n==== Operation Failed !  Invalid value entered ====\n")
        return False

    def storage(self, value):
        if value > 0:
            self._balance += value
            print("\n==== Valid Operation ! Deposit successfully made ====\n")
        else:
            print("\n==== Operation Failed ! Invalid value entered =====\n")
            return False
        return True


class CurrentAccount(Account):
    def __init__(self, number, client):
        self._limit = 500
        self._limit_draw = 3
        super().__init__(number, client)

    def draw(self, value):
        number_draws = len(
            [
                transaction
                for transaction in self.historic.transactions
                if transaction["type"] == Draw.__name__
            ]
        )
        exceed_limit = value > self._limit
        exceed_draws = number_draws >= self._limit_draw
        if exceed_limit:
            print("\n==== Operation Failed ! The withdrawal exceeds your limit ====\n")
        elif exceed_draws:
            print(
                "\n==== Operation Failed ! The maximum number of withdrawals has been exceeded ====\n"
            )
        else:
            return super().draw(value)
        return False

    def __str__(self):
        return f"""\
            Agency:\t{self._agency}
            C/C:\t\t{self._number}
            Header:\t{self._client._name}
        """


class Historic:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction._value,
            }
        )


class Client:
    def __init__(self, address):
        self._address = address
        self._accounts = []

    def add_account(self, account):
        self._accounts.append(account)

    def transaction_call(self, account, transaction):
        if account in self._accounts:
            transaction.register(account)


class Individual(Client):
    def __init__(self, cpf, name, birthday, address):
        self._cpf = cpf
        self._name = name
        self._birthday = birthday
        super().__init__(address)


class Transaction(ABC):
    @property
    @abstractproperty
    def value(self):
        pass

    @abstractclassmethod
    def register(self, account):
        pass


class Storage(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        successful_transaction = account.storage(self._value)
        if successful_transaction:
            account.historic.add_transaction(self)


class Draw(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        successful_transaction = account.draw(self._value)
        if successful_transaction:
            account.historic.add_transaction(self)


def filter_client(cpf, clients):
    clients_filtered = [client for client in clients if client._cpf == cpf]
    return clients_filtered[0] if clients_filtered else None


def recover_account(client):
    if not client._accounts:
        print("\n==== Client dont have account ! ====\n")
        return
    elif len(client._accounts) == 1:
        return client._accounts[0]
    else:
        for account in client._accounts:
            print(f"\nNúmero da conta: \t{account._number}")
            print(f"Saldo: \t{account._balance}")
            print("-" * 20)
        number_Account = input("\nEnter the account number: ")
        while not number_Account or not any(
            account._number == number_Account for account in client._accounts
        ):
            number_Account = input("\n Invalid number ! Try again: ")
        account_choice = next(
            account for account in client._accounts if account._number == number_Account
        )
        return account_choice


def storage(clients):
    cpf = input("Client CPF: ")
    client = filter_client(cpf, clients)
    if not client:
        print("\n==== Not Found Client ! ====\n")
        return
    value = float(input("Deposit value: "))
    transaction = Storage(value)
    account = recover_account(client)
    if not account:
        return

    client.transaction_call(account, transaction)


def draw(clients):
    cpf = input("Client CPF: ")
    client = filter_client(cpf, clients)
    if not client:
        print("\n==== Not Found Client ! ====\n")
        return
    value = float(input("Withdrawal value: "))
    transaction = Draw(value)
    account = recover_account(client)
    if not account:
        return

    client.transaction_call(account, transaction)


def extract(clients):
    cpf = input("Client CPF: ")
    client = filter_client(cpf, clients)
    if not client:
        print("\n==== Not Found Client ! ====\n")
        return
    account = recover_account(client)
    if not account:
        return
    print("\n============= EXTRACT =============\n")
    transactions = account.historic.transactions

    extract = ""
    if not transactions:
        extract = "Not found transactions in this account !"
    else:
        for transaction in transactions:
            extract += f"\n{transaction['type']}:\n\tR$ {transaction['value']:.2f}"
    print(extract)
    print(f"\nSaldo: \n\tR$ {account._balance:.2f}")
    print("\n==========================\n")


def create_client(clients):
    cpf = input("Client CPF: ")
    client = filter_client(cpf, clients)
    if client:
        print("\n==== Client Already Exists ! ====\n")
        return
    name = input("Enter with your name: ")
    birthday = input("Enter with your date of birthday (dd-mm-aaaa): ")
    address = input("Enter your address (street, number - area - city): ")

    client = Individual(cpf=cpf, name=name, birthday=birthday, address=address)
    clients.append(client)
    print("\n==== Registered client ====\n")


def create_account(number_account, clients, accounts):
    cpf = input("Client CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n==== Client not Found ! Try again =====\n")
        return

    account = CurrentAccount.new_account(client=client, number=number_account)
    accounts.append(accounts)
    client._accounts.append(account)

    print("\n=== Account successfully created ! ===")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdrawal
    [3]\tExtract
    [4]\tNew Client
    [5]\tNew Account
    [6]\tList Accounts
    [7]\tExit
    => """
    return input(textwrap.dedent(menu))


def main():
    clients = []
    accounts = []
    while True:
        option = menu()
        if option == "1":
            storage(clients)
        elif option == "2":
            draw(clients)
        elif option == "3":
            extract(clients)
        elif option == "4":
            create_client(clients)
        elif option == "5":
            number_account = len(accounts) + 1
            create_account(number_account, clients, accounts)
        elif option == "6":
            list_accounts(accounts)
        elif option == "7":
            print("\n--- Saindo do programa ! ---\n")
            break
        else:
            print("\n--- Operação Invalida ! Tente novamente ---\n")


main()
