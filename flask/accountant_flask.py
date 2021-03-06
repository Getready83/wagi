from flask import Flask, render_template, request, redirect
import sys


class Manager:
    def __init__(self):
        self.actions = {}
        self.list = []
        self.log = []
        self.account = 0
        self.warehouse = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
            return cb
        return decorate

    def execute(self, name):
        if name not in self.actions:
            print(f"Action not defined: {name}")
        else:
            action = self.actions[name](self)
            status = action.access_request(request)
            if action.execute():
                self.log.append(action)
                with open('konto1.txt', "w") as file:
                    for action in self.log:
                        action.write(file)
                return True, self.warehouse
            return False, self.warehouse

    def read_parameters(self, numbers_line, source, file=None):
        self.list = []
        status = True
        if source == "file":
            for line_number in range(numbers_line):
                line = file.readline()
                if not line:
                    return False, self.list
                line = line.strip()
                self.list.append(line)
            return True, self.list
        if source == "argv":
            if len(sys.argv) >= numbers_line + 1:
                self.list.append(sys.argv[1:])
                return True, sys.argv[1:numbers_line + 1]
            else:
                return False, sys.argv[1:]

    def main_loop(self):
        with open("konto1.txt", 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.strip()
                if line in self.actions:
                    action = self.actions[line](self)
                    status = action.access_file("file", file)
                    if not status:
                        break
                    status = action.execute()
                    if not status:
                        break
                    self.log.append(action)
            with open('konto1.txt', "w") as file:
                for action in self.log:
                    action.write(file)
                return self.account


def create_manager():
    manager = Manager()

    @manager.assign("saldo")
    class AccountBalance:
        def __init__(self, manager):
            self.manager = manager
            self.amount = 0
            self.comment = ""
            self.list = []

        def access_file(self, source, file=None):
            status, self.list = manager.read_parameters(2, source, file)
            if not status:
                print("error - incorrect parameters for saldo")
                return False
            self.amount = int(self.list[0])
            self.comment = self.list[1]
            return True

        def access_argv(self, source, file=None):
            status, self.list = manager.read_parameters(2, source, file)
            if not status:
                print("error - incorrect parameters for saldo")
                return False
            self.amount = int(sys.argv[2])
            self.comment = sys.argv[3]
            return True

        def access_request(self, request):
            self.amount = request.form.get("amount")
            if not self.amount:
                print("No parameters")
            self.comment = (request.form.get("comment"))
            if not self.comment:
                print("No parameters")
            return

        def execute(self):
            if int(self.amount) + int(self.manager.account) < 0:
                print("error")
                return False
            else:
                self.manager.account += int(self.amount)
                return True

        def write_html(self):
            return "saldo", self.amount, self.comment

        def write(self, file):
            file.write("saldo\n")
            file.write(f"{self.amount}\n")
            file.write(f"{self.comment}\n")
            return self.amount, self.comment


    @manager.assign("zakup")
    class Buy:
        flag_action = "zakup"
        error = "error - incorrect parameters for buy"

        def __init__(self, manager):
            self.manager = manager
            self.name = ""
            self.price = 0
            self.quantity = 0
            self.list = []

        def access_file(self, source, file=None):
            status, self.list = manager.read_parameters(3, source, file)
            if not status:
                print(self.error)
                return False
            self.name = (self.list[0])
            self.price = int(self.list[1])
            self.quantity = int(self.list[2])
            return True

        def access_argv(self, source, file=None):
            status, self.list = manager.read_parameters(3, source, file)
            if not status:
                print(self.error)
                return False
            self.name = (sys.argv[2])
            self.price = int(sys.argv[3])
            self.quantity = int(sys.argv[4])
            return True

        def access_request(self, request):
            if not request.form.get("name"):
                return False, request.form.get("incorrect buy")
            else:
                self.name = request.form.get("name")
                try:
                    self.price = int(request.form.get("price", 0))
                except ValueError:
                    return False
                try:
                    self.quantity = int(request.form.get("quantity", 0))
                except ValueError:
                    return 0
                if self.price == 0:
                    return False
                if self.quantity == 0:
                    return False
                return True, self.name, self.price, self.quantity

        def execute(self):
            if self.manager.account - (self.price * self.quantity) < 0:
                print("You have no funds in your account")
                return False
            else:
                if self.name not in self.manager.warehouse:
                    self.manager.warehouse[self.name] = self.quantity
                    self.manager.account -= self.price * self.quantity
                else:
                    self.manager.warehouse[self.name] += self.quantity
                    self.manager.account -= self.price * self.quantity
                return True, self.manager.account, self.manager.warehouse

        def write_html(self):
            return "zakup", self.name, self.price, self.quantity

        def write(self, file):
            file.write(f"{self.flag_action}\n")
            file.write(f"{self.name}\n")
            file.write(f"{self.price}\n")
            file.write(f"{self.quantity}\n")

    @manager.assign("sprzedaz")
    class Sell(Buy):
        def __init__(self, manager):
            super().__init__(manager)

        def access_file(self, source, file=None):
            self.error = "error - incorrect parameters for sell"
            super().access_file(source, file)
            return True

        def access_argv(self, source, file=None):
            self.error = "error - incorrect parameters for sell"
            super().access_argv(source, file)
            return True

        def access_request(self, request):
            self.name = request.form.get("name1")
            if not self.name:
                print("No parameters for Sell")
            try:
                self.price = int(request.form.get("price", 0))
                if not self.price:
                    print("No parameters for Sell")
            except ValueError:
                return 0
            try:
                self.quantity = int(request.form.get("quantity", 0))
                if not self.quantity:
                    print("No parameters for Sell")
            except ValueError:
                return 0
            return True, self.name, self.price, self.quantity

        def execute(self):
            if self.name not in self.manager.warehouse:
                print("Product not in stock.")
                return False
            else:
                if self.manager.warehouse[self.name] - self.quantity < 0:
                    print("error - there is not enough quantity in stock")
                    return False
                else:
                    self.manager.warehouse[self.name] -= self.quantity
                    self.manager.account += self.price * self.quantity
                    return True, self.manager.account, self.manager.warehouse

        def write_html(self):
            return "sprzedaz", self.name, self.price, self.quantity

        def write(self, file):
            self.flag_action = "sprzedaz"
            super().write(file)


    @manager.assign("konto")
    class Account(AccountBalance):

        def access_file(self, source, file=None):
            return True

        def access_argv(self, source, file=None):
            return True

        def execute(self):
            print(self.manager.account)
            return self.manager.account

        def write_html(self):
            return

        def write(self, file):
            file.write("saldo\n")
            file.write(f"{self.amount}\n")
            file.write(f"{self.comment}\n")
            return self.amount, self.comment



    @manager.assign("magazyn")
    class Warehouse:
        def __init__(self, manager):
            self.manager = manager

        def access_file(self, source, file=None):
            return True

        def access_argv(self, source, file=None):
            return True

        def access_request(self, request):
            return

        def execute(self):
            with open("warehouse.txt", "w")as file:
                for self.name in sys.argv[2:]:
                    file.write(
                        f"{self.name}: {self.manager.warehouse[self.name]}\n"
                    ) if self.name in self.manager.warehouse else file.write(
                        f"{self.name}: {0}\n"
                    )
            return self.manager.warehouse

        def write_html(self):
            return self.name, self.price, self.quantity

        def write(self, file):
            for self.name in sys.argv[2:]:
                file.write(
                    f"{self.name}: {self.manager.warehouse[self.name]}\n"
                ) if self.name in self.manager.warehouse else file.write(
                    f"{self.name}: {0}\n"
                )
            return

    @manager.assign("przeglad")
    class Overview:
        def __init__(self, manager):
            self.manager = manager

        def access_file(self, source, file=None):
            return True

        def access_argv(self, source, file=None):
            from_line = sys.argv[2]
            to_line = sys.argv[3]
            return True

        def access_request(self, request):
            return

        def execute(self):
            with open("overview.txt", "w") as file:
                for action in self.manager.log[
                              int(request.form.get("line_from",0)): int(
                                  request.form.get("line_to", len(
                                      self.manager.log)-1)) + 1
                              ]:
                    action.write(file)
                return

        def write(self):
            with open("overview", "w") as file:
                for action in self.manager.log[
                        int(self.from_line): int(self.to_line) + 1
                        ]:
                    for event in action.write(file):
                        event.write(file)

    action_type = {"saldo": AccountBalance, "zakup": Buy, "sprzedaz": Sell}

    return manager, action_type
