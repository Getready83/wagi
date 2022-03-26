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

        for event in db.session.query(Transaction):
            self.transaction.append(event.transaction)

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
            print(action,"1111")
            action.access_request(request)
            action.execute()
            self.log.append(action)
            for action in self.log:
                action.write_db()
            return True, self.warehouse

    def main_loop(self, request):
        while True:
            line = request.form.get("action")
            if line in self.actions:
                action = self.actions[line](self)
                status = action.access_request(request)
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

        def access_request(self, request):
            self.amount = int(request.form.get("amount"))
            self.comment = (request.form.get("comment"))
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
                return True

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
    class Sell(Buy):
        def __init__(self, manager):
            super().__init__(manager)

        def access_request(self, request):
            self.name = request.form.get("name1")
            self.price = int(request.form.get("price", 0))
            self.quantity = int(request.form.get("quantity", 0))

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
            self.flag_action = "sprzedaz"
            super().write(file)

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


    @manager.assign("konto")
    class Account(AccountBalance):

        def execute(self):
            print(self.manager.account)
            return self.manager.account

        def write_html(self):
            return

        def write_db(self):
            pass

    @manager.assign("magazyn")
    class Warehouse:
        def __init__(self, manager):
            self.manager = manager

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
                return

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

        def access_request(self, request):
            from_line = int(request.form.get("line_from", 0))
            to_line = int(request.form.get("line_to", len(manager.log)-1))
            return

        def execute(self):
            for action in self.manager.log[
                          int(request.form.get("line_from",0)): int(
                              request.form.get("line_to", len(
                                  self.manager.log)-1)) + 1
                          ]:
                action.write_db()
            return

        def write(self):
            for action in self.manager.transaction[
                    int(self.from_line): int(self.to_line) + 1
                    ]:
                for event in action.write_html():
                    event.write_html()

        def write_db(self):
            for action in self.manager.transaction[
                          int(self.from_line): int(self.to_line) + 1
                          ]:
                for event in action.write_html():
                    event.write_html()

    action_type = {"saldo": AccountBalance, "zakup": Buy, "sprzedaz": Sell}

    return manager, action_type

@new.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.main_loop(request)
    status, warehouse = manager.execute("magazyn")
    action = request.form.get("action")
    print(action, "action hello")
    error = {"zakup": "", "sprzedaz": "", "saldo": ""}
    if action in action_type:
        print(action, " 386")
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


@new.route("/history/", methods=["GET", "POST"])
def hello2():
    log = {}
    manager, action_type = create_manager()
    manager.main_loop(request)
    for t in db.session.query(Transaction).all():
        log[t.transaction] = t.comment_or_name, t.value_or_price, t.quantity
    print(log)
    from_line = int(request.form.get("line_from", 0))
    to_line = int(request.form.get("line_to", len(manager.log)-1))

    """log = {}
    manager, action_type = create_manager()
    manager.main_loop(request)
    from_line = int(request.form.get("line_from", 0))
    to_line = int(request.form.get("line_to", len(manager.log)-1))
    manager.execute("przeglad")"""

    return render_template(
        "history.html", manager=manager, from_line=from_line, to_line=to_line,
        log=manager.log[from_line:to_line+1]
    )


@new.route("/thanks/", methods=["Get", "POST"])
def thankyou():
    return render_template("thanks.html")


new.run(debug=True)
