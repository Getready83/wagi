from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
import sys

new = Flask(__name__)
new.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(new)

alembic = Alembic()
alembic.init_app(new)


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
    transaction = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float,  nullable=False)
    comment = db.Column(db.String(30), nullable=False)


class AccountDb(db.Model):
    finances = db.Column(db.Float, primary_key=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction = db.Column(db.String(10))
    comment_or_name = db.Column(db.String)
    value_or_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

db.create_all()

class Manager:
    def __init__(self):
        self.actions = {}
        self.transaction = []
        self.log = []
        self.account = 0
        self.warehouse = {}
        self.overview = []
        self.load()

    def load(self):
        for product in db.session.query(WarehouseDb):
            self.warehouse[product.product_name] = product.product_quantity

        for buy_db in db.session.query(BuyDb):
            self.transaction.append(buy_db.transaction)

        for sell_db in db.session.query(SellDb):
            self.transaction.append(sell_db.transaction)

        for saldo_db in db.session.query(SaldoDb):
            self.transaction.append(saldo_db.transaction)

        for money in db.session.query(AccountDb):
            self.account = money.finances

        for event in db.session.query(Transaction).all():
            self.transaction.append(event)


    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
            return cb
        return decorate

    def execute(self, name):
        finances = db.session.query(AccountDb).first()
        finances.finances = self.account
        db.session.add(finances)
        db.session.commit()
        if name not in self.actions:
            print(f"Action not defined: {name}")
        else:
            action = self.actions[name](self)
            action.access_request(request)
            action.execute()
            print(action.execute, "line 97")
            self.log.append(action)
            print(self.log, " 98")
            print(action.write_html(), "line 99")
            action.write_db()
        return True, self.warehouse

    def main_loop(self, request):
        while True:
            line = request.form.get("action")
            print(line, "105")
            if line in self.actions:
                action = self.actions[line](self)
                status = action.access_request(request)
                print(status,"1")
                action.execute()
                print(action.execute,"111 linia")
                print(status,"2")
                self.log.append(action)
            print(self.log, "linia 117")
            return self.account

    def read(self, from_line, to_line):
        for transaction in db.session.query(Transaction).all():
            self.transaction.append(transaction)
            print(transaction.id, transaction.transaction,
                  transaction.comment_or_name, transaction.value_or_price,
                  transaction.quantity)



def create_manager():
    manager = Manager()

    @manager.assign("saldo")
    class AccountBalance:
        def __init__(self, manager):
            self.manager = manager
            self.amount = 0
            self.comment = ""

        def access_request(self, request):
            self.amount = int(request.form.get("amount"))
            self.comment = (request.form.get("comment"))
            self.manager.overview.append(self.amount)
            self.manager.overview.append(self.comment)
            return self.manager.overview


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

        def write_db(self):
            event_in_transaction = Transaction(
                transaction="saldo", comment_or_name=self.comment,
                value_or_price=self.amount, quantity="----")
            event_in_saldo = SaldoDb(transaction="saldo",
                                     value=self.amount, comment=self.comment)
            db.session.add(event_in_saldo)
            db.session.add(event_in_transaction)
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
            print(self.quantity, "171")

        def access_request(self, request):
            self.name = request.form.get("name")
            self.price = int(request.form.get("price", 0))
            print(self.price, "176 acces request zakup pri")
            self.quantity = int(request.form.get("quantity", 0))
            print(self.quantity, "178 acces request zakup qty")
            self.manager.overview.append(self.name)
            self.manager.overview.append(self.price)
            self.manager.overview.append(self.quantity)
            return self.manager.overview

        def execute(self):
            if self.manager.account - (self.price * self.quantity) < 0:
                print("You have no funds in your account")
            else:
                if self.name not in self.manager.warehouse:
                    self.manager.warehouse[self.name] = self.quantity
                    self.manager.account -= self.price * self.quantity
                else:
                    self.manager.warehouse[self.name] += self.quantity
                    self.manager.account -= self.price * self.quantity
            print(manager.overview, "194")
        def write_html(self):
            return "zakup", self.name, self.price, self.quantity


        def write_db(self):
            event_in_transaction = Transaction(
                transaction="zakup", comment_or_name=self.name, value_or_price=
            self.price, quantity=self.quantity)
            event_in_buy = BuyDb(transaction="zakup",
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
            db.session.add(event_in_transaction)
            db.session.commit()


    @manager.assign("sprzedaz")
    class Sell():
        def __init__(self, manager):
            self.manager = manager
            self.name = ""
            self.price = 0
            self.quantity = 0

        def access_request(self, request):
            self.name = request.form.get("name1")
            self.price = int(request.form.get("price", 0))
            self.quantity = int(request.form.get("quantity", 0))
            self.manager.overview.append(self.name)
            self.manager.overview.append(self.price)
            self.manager.overview.append(self.quantity)
            return self.manager.overview

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
                return True

        def write_html(self):
            return "sprzedaz", self.name, self.price, self.quantity

        def write(self, file):
            file.write(f"{self.flag_action}\n")
            file.write(f"{self.name}\n")
            file.write(f"{self.price}\n")
            file.write(f"{self.quantity}\n")

        def write_db(self):
            event_in_transaction = Transaction(
                transaction="sprzedaz", comment_or_name=self.name, value_or_price=
                self.price, quantity=self.quantity)
            event_in_sell = SellDb(transaction="sprzedaz",
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
            db.session.add(event_in_sell)
            db.session.add(event_in_transaction)
            db.session.commit()

    @manager.assign("przeglad")
    class Overview:
        def __init__(self, manager):
            self.manager = manager

        def access_request(self, request):
            from_line = int(request.form.get("line_from", 0))

            to_line = int(request.form.get("line_to", len(
                self.manager.log) - 1)) + 1
            return from_line, to_line

        def execute(self):
            with open("overview.txt", "w") as file:
                for action in self.manager.log[
                              int(request.form.get("line_from", 0)): int(
                                  request.form.get("line_to", len(
                                      self.manager.log) - 1)) + 1
                              ]:
                    action.write(file)
                return

        def write_html(self):
            return True

        def write_db(self):
            pass

    action_type = {"saldo": AccountBalance, "zakup": Buy, "sprzedaz": Sell}

    return manager, action_type

@new.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.main_loop(request)
    status, warehouse = manager.execute(request)
    if request.method == "POST":
        action = request.form.get("action")
        error = {"zakup": "", "sprzedaz": "", "saldo": ""}
        print(request.method, "request method")
        print(request.form, "request form")
        print(action, "action")
        if action in action_type:
            status, warehouse = manager.execute(action)
            if status:
                return redirect("/")
            else:
                error[action] = "incorrect data"
        return render_template(
                "accountant.html",
                manager=manager, account=account, warehouse=warehouse,
             form=request.form, error=error, status=status
                            )
    return render_template(
                "accountant.html", manager=manager, account=account, warehouse=warehouse, form=request.form, error="")

@new.route("/history/", methods=["GET", "POST"])
def hello2():
    manager, action_type = create_manager()
    log = []
    manager.main_loop(request)
    from_line = int(request.form.get("line_from", 0))
    to_line = int(request.form.get("line_to", len(manager.transaction)-1))
    if request.method == "POST":
        manager.read(from_line, to_line)
        return redirect("/history/")

    return render_template(
        "history.html", manager=manager, from_line=from_line, to_line=to_line,
        log=manager.transaction[from_line:to_line+1]
    )


    """
    log = {}
    manager, action_type = create_manager()
    manager.main_loop(request)
    print(manager.main_loop(request), "315")
    from_line = int(request.form.get("line_from", 0))
    to_line = int(request.form.get("line_to", len(manager.log)-1))
    manager.execute(request)
    print(manager.execute("przeglad"), 319)


    for t in db.session.query(Transaction).all():
        log[t.transaction] = t.comment_or_name, t.value_or_price, t.quantity
    print(log)
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
"""

@new.route("/thanks/", methods=["Get", "POST"])
def thankyou():
    return render_template("thanks.html")



new.run(debug=True)
