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
            self.log.append(action)
            action.write_db()
        return self.warehouse

    def main_loop(self, request):
        while True:
            line = request.form.get("action")
            if line in self.actions:
                action = self.actions[line](self)
                status = action.access_request(request)
                action.execute()
                self.log.append(action)
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
            print(self.amount,"saldo amout")
            self.comment = (request.form.get("comment"))
            print(self.comment, "saldo comm")
            return

        def execute(self):
            if int(self.amount) + int(self.manager.account) < 0:
                print("error")
                return False
            else:
                self.manager.account += int(self.amount)
                return True

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

        def access_request(self, request):
            self.name = request.form.get("name")
            self.price = int(request.form.get("price", 0))
            print(self.price, "self.price zakup")
            self.quantity = int(request.form.get("quantity", 0))
            print(self.quantity, "zakup")
            return

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
            self.price = int(request.form.get("price1", 0))
            print(self.price, "price sprzedaz")
            self.quantity = int(request.form.get("quantity1", 0))
            print(self.quantity,"qty sprzedaz")
            return

        def execute(self):
            if self.name not in self.manager.warehouse:
                print("Product not in stock.")
                return False
            else:
                if self.manager.warehouse[self.name] - self.quantity < 0:
                    print("error - there is not enough quantity in stock")
                    del self.quantity
                    return False
                else:
                    self.manager.warehouse[self.name] -= self.quantity
                    self.manager.account += self.price * self.quantity
                return True

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

    action_type = {"saldo": AccountBalance, "zakup": Buy, "sprzedaz": Sell}

    return manager, action_type

@new.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.main_loop(request)
    warehouse = manager.execute(request)
    if request.method == "POST":
        action = request.form.get("action")
        error = {"zakup": "", "sprzedaz": "", "saldo": ""}
        print(request.method, "request method")
        print(request.form, "request form")
        print(action, "action")
        if action in action_type and False:
            status = manager.execute(action)
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
    for transaction in db.session.query(Transaction).all():
        log.append(transaction)
    from_line = int(request.form.get("line_from", 0))
    if not request.form.get("line_from", 0):
        from_line = 0
    to_line = int(request.form.get("line_to", len(log)-1))
    if not request.form.get("line_to", len(log)-1):
        to_line = len(log)-1
    for transaction in db.session.query(Transaction).all():
        log.append(transaction)

    return render_template(
        "history.html", manager=manager, from_line=from_line, to_line=to_line,
        log=log[from_line:to_line+1]
    )


@new.route("/thanks/", methods=["Get", "POST"])
def thankyou():
    return render_template("thanks.html")



new.run(debug=True)
