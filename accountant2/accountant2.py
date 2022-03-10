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
            action.access_argv("argv")
            if action.execute():
                self.log.append(action)

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
                print(self.list)
                return True, sys.argv[1:numbers_line + 1]
            else:
                return False, sys.argv[1:]

    def main_loop(self):
        with open(sys.argv[1], 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.strip()
                if line in action_type:
                    action = action_type[line](manager)
                    status = action.access_file("file", file)
                    if not status:
                        break
                    status = action.execute()
                    if not status:
                        break
                    self.log.append(action)
            with open('konto.txt', "w") as file:
                print(self.log)
                for action in self.log:
                    action.write(file)
            return self.account, self.list


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
            print("error - incorrect parameters for account")
            return False
        self.amount = int(sys.argv[2])
        self.comment = sys.argv[3]
        return True

    def execute(self):
        if self.amount + self.manager.account < 0:
            print("error")
            return False, self.manager.account
        self.manager.account += self.amount
        return True

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
        print(self.name, self.price, self.quantity)
        return True

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

    def write(self, file):
        file.write(f"{self.flag_action}\n")
        file.write(f"{self.name}\n")
        file.write(f"{self.price}\n")
        file.write(f"{self.quantity}\n")
        return self.name, self.price, self.quantity


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

    def execute(self):
        if self.name not in self.manager.warehouse:
            print("Product not in stock.")
            return False, self.manager.account, self.manager.warehouse
        else:
            if self.manager.warehouse[self.name] - self.quantity < 0:
                print("error - there is not enough quantity in stock")
                return False, self.manager.account, self.manager.warehouse,\
                       self.manager.warehouse[self.name]
            else:
                self.manager.warehouse[self.name] -= self.quantity
                self.manager.account += self.price * self.quantity
            return True, self.manager.account, self.manager.warehouse

    def write(self, file):
        self.flag_action = "sprzedaz"
        super().write(file)


@manager.assign("konto")
class Account:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        print(self.manager.account)


@manager.assign("magazyn")
class Warehouse:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        with open("magazyn.txt", "w") as file:
            pass


@manager.assign("przeglad")
class Review:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        with open("przeglad.txt", "w") as file:
            for action in self.log[int(sys.argv[2]): int(sys.argv[3]) + 1]:
                print(action.write(file))
                return action.write(file)


action_type = {"saldo": AccountBalance, "zakup": Buy, "sprzedaz": Sell}








           


