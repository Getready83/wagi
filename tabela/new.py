from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sys

new = Flask(__name__)
new.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(new)


class WarehouseDb(db.Model):
    product_name = db.Column(db.String(30), primary_key=True)
    product_quantity = db.Column(db.Integer)


class BuyDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String(10), unique=False, nullable=False)
    product_name = db.Column(db.String(30), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    qty_product = db.Column(db.Integer, unique=False, nullable=False)


class SellDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String(10), unique=False, nullable=False)
    product_name = db.Column(db.String(30), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    qty_product = db.Column(db.Integer, unique=False, nullable=False)


class SaldoDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String(10), unique=False, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)
    comment = db.Column(db.String(30), unique=False, nullable=False)


class AccountDb(db.Model):
    finances = db.Column(db.Float, primary_key=True)


ada = db.session.query(AccountDb).first()
print(ada)


class Manager:
    def __init__(self):
        self.actions = {}
        self.transaction = []
        self.log = []
        self.account = 0
        self.warehouse = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
            return cb
        return decorate

    def execute(self, name):

        for product in db.session.query(WarehouseDb):
            self.warehouse[product.name] = product.quantity

        for product in db.session.query(BuyDb):
            self.transaction.append(product.to_buy)

        for product in db.session.query(SellDb):
            self.transaction.append(product.to_sell)

        for t in db.session.query(SaldoDb):
            self.transaction.append(t.transaction)

        for money in db.session.query(AccountDb):
            self.account = money.finances

        print(money, "money.finances")

        if name not in self.actions:
            print(f"Action not defined: {name}")
        else:
            action = self.actions[name](self)
            print(action, "manager execute")
            action.access_request(request)
            action.execute()
            self.log.append(action)
            for action in self.log:
                action.write_db()
            return True, self.warehouse, self.account, self.transaction, self.log
        return False, self.warehouse, self.account, self.transaction, self.log

    def main_loop(self, request):
        while True:
            line = request.form.get("action")
            print(line, "linia po request")
            if line in self.actions:
                print(self.actions, "main_loop")
                action = self.actions[line](self)
                print(action, "main_ loop linia 97")
                status = action.access_request(request)
                print("status0")
                if not status:
                    break
                status = action.execute()
                if not status:
                    break
                self.log.append(action)
            for action in self.log:
                action.write_db()
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

        def access_request(self, request):
            self.amount = int(request.form.get("amount"))
            self.comment = (request.form.get("comment"))
            return True

        def execute(self):
            if int(self.amount) + int(self.manager.account) < 0:
                print("error")
                return False
            else:
                self.manager.account += int(self.amount)
                return True

        def write_html(self):
            return "saldo", self.amount, self.comment

        def write_db(self):
            id_saldo = db.session.query(SaldoDb).filter(SaldoDb.id).all()
            id_saldo = 1
            event_in_saldo = SaldoDb(id=id_saldo, transaction="saldo",
                                     value=self.amount, comment=self.comment)
            finances = db.session.query(AccountDb).first()
            finances.finances = self.manager.account
            db.session.add(event_in_saldo)
            db.session.add(finances)
            db.session.commit()

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

        def access_request(self, request):
            self.name = request.form.get("name")
            self.price = int(request.form.get("price", 0))
            self.quantity = int(request.form.get("quantity", 0))
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

        def write_db(self):
            finances = db.session.query(AccountDb).first()
            finances.finances = self.manager.account
            id_buy = db.session.query(BuyDb).filter(BuyDb.id).all()
            id_buy = id_buy[1] + 1
            event_in_buy = BuyDb(id=id_buy, transaction="zakup",
                                 product_name=self.name, price=self.price,
                                 qty_product=self.quantity)
            warehouse_db = db.session.query(WarehouseDb).filter(
                WarehouseDb.product_name == self.name).first()
            if not warehouse_db:
                warehouse_db = WarehouseDb(product_name=self.name,
                                           product_quantity=self.quantity)
            else:
                warehouse_db.product_quantity = self.manager.warehouse[self.name]
            db.session.add(warehouse_db)
            db.session.add(event_in_buy)
            db.session.commit()


    @manager.assign("sprzedaz")
    class Sell(Buy):
        def __init__(self, manager):
            super().__init__(manager)

        def access_request(self, request):
            self.name = request.form.get("name1")
            self.price = int(request.form.get("price", 0))
            self.quantity = int(request.form.get("quantity", 0))
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

        def write_db(self):
            finances = db.session.query(AccountDb).first()
            finances.finances = self.manager.account
            id_sell = db.session.query(BuyDb).filter(BuyDb.id).all()
            id_sell = 1
            event_in_buy = BuyDb(id=id_sell, transaction="sprzedaz",
                                 product_name=self.name, price=self.price,
                                 qty_product=self.quantity)
            warehouse_db = db.session.query(WarehouseDb).filter(
                WarehouseDb.product_name == self.name).first()
            if not warehouse_db:
                warehouse_db = WarehouseDb(product_name=self.name,
                                           product_quantity=self.quantity)
            else:
                warehouse_db.product_quantity = self.manager.warehouse[self.name]
            db.session.add(warehouse_db)
            db.session.add(event_in_buy)
            db.session.commit()


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

        def write_db(self):
            pass


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

        def write_db(self):
            pass

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

        def write_db(self):
            pass

    action_type = {"saldo": AccountBalance, "zakup": Buy, "sprzedaz": Sell}

    return manager, action_type

@new.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.main_loop(request)
    status, warehouse, manager.account, manager.transaction, manager.log = manager.execute("magazyn")
    action = request.form.get("action")
    error = {"zakup": "", "sprzedaz": "", "saldo": ""}
    if action in action_type:
        status, warehouse, manager.account, manager.transaction, manager.log= manager.execute(action)
        if status:
            return redirect("/")
        else:
            error[action] = "incorrect data"
    return render_template(
            "accountant.html",
            manager=manager, account=account, warehouse=warehouse,
         form=request.form, error=error, status=status
                        )


@new.route("/history/", methods=["GET", "POST"])
def hello2():
    log = {}
    manager, action_type = create_manager()
    manager.main_loop(request)
    from_line = int(request.form.get("line_from", 0))
    to_line = int(request.form.get("line_to", len(manager.log)-1))
    manager.execute("przeglad")

    return render_template(
        "history.html", manager=manager, from_line=from_line, to_line=to_line,
        log=manager.log[from_line:to_line+1]
    )


@new.route("/thanks/", methods=["Get", "POST"])
def thankyou():
    return render_template("thanks.html")


new.run(debug=True)
