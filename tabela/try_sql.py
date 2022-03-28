from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sys

try_sql = Flask(__name__)
try_sql.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(try_sql)


class WarehouseDb(db.Model):
    product_name = db.Column(db.String(30), primary_key=True)
    product_quantity = db.Column(db.Integer, unique=False, nullable=False)



class History(db.Model):
    transaction = db.Column(db.String(10), primary_key=True)
    product_name = db.Column(db.String(30), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    qty_product = db.Column(db.Integer, unique=False, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)
    comment = db.Column(db.String(30), unique=False, nullable=False)
    finances = db.Column(db.Float, unique=False, nullable=False)

db.create_all()


class Manager:
    def __init__(self):
        self.actions = {}
        self.warehouse = {}
        self.list = []
        self.log = []
        self.account = 0

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb        #cb = klasa
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
                for action in self.log:
                    action.write_db()
                return True, self.warehouse
            return False, self.warehouse


    def main_loop(self):
        while True:
            line = request.form.get("action")
            if line in self.actions:
                action = self.actions[line](self)
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

        def write_db(self):
            finances = db.session.query(History).filter(History.finances).all()
            finances.finances = self.manager.account
            event_in_history = db.session.query(History).filter(History.transaction=="saldo").first()
            event_in_history = History(
                transaction="saldo", value=self.amount, comment=self.comment
            )
            db.session.add(event_in_history)
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

        def write_db(self):
            event_in_history = db.session.query(History).filter(History.finances).all()
            event_in_history.finances = self.manager.account
            event_in_history = db.session.query(History.transaction).filter(
                History.transaction == "zakup").first()
            event_in_history = History(
                transaction="zakup", product_name=self.name, price=self.prise, qty=self.quantity
            )
            warehouse_db = db.session.query(WarehouseDb).filter(WarehouseDb.product_name==self.name).first()
            if not WarehouseDb:
                warehouse_db = WarehouseDb(product_name=self.name, qty=self.quantity)
            else:
                qty = self.manager.warehouse[self.name]
            db.session.add(warehouse_db)
            db.session.add(event_in_history)
            db.session.commit()

    @manager.assign("sprzedaz")
    class Sell(Buy):
        def __init__(self, manager):
            super().__init__(manager)

        def access_request(self, request):
            if not request.form.get("name"):
                return False, request.form.get("incorrect sell")
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
            event_in_history = db.session.query(History).filter(History.finances).all()
            event_in_history.finances = self.manager.account
            event_in_history = db.session.query(History.transaction).filter(
                History.transaction == "sprzedaz").first()
            event_in_history = History(
                transaction="sprzedaz", product_name=self.name, price=self.prise, qty=self.quantity
            )
            warehause_db = db.session.query(WarehouseDb).filter(WarehouseDb.product_name==self.name).first()
            if not WarehouseDb:
                warehause_db = WarehouseDb(product_name=self.name, qty=self.quantity)
            else:
                qty = self.manager.warehouse[self.name]
            db.session.add(warehouse_db)
            db.session.add(event_in_history)
            db.session.commit()

    @manager.assign("konto")
    class Account(AccountBalance):


        def execute(self):
            print(self.manager.account)
            return self.manager.account

        def access_request(self, request):
            return True

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

        def access_request(self, request):
            return True

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


tryme = Flask(__name__)


@tryme.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.account
    status, warehouse = manager.execute("magazyn")
    action = request.form.get("action")
    error = {"zakup": "", "sprzedaz": "", "saldo": ""}
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


@tryme.route("/history/", methods=["GET", "POST"])
def hello2():
    log = {}
    manager, action_type = create_manager()
    manager.main_loop()
    from_line = int(request.form.get("line_from", 0))
    to_line = int(request.form.get("line_to", len(manager.log)-1))
    manager.execute("przeglad")

    return render_template(
        "history.html", manager=manager, from_line=from_line, to_line=to_line,
        log=manager.log[from_line:to_line+1]
    )


@tryme.route("/thanks/", methods=["Get", "POST"])
def thankyou():
    return render_template("thanks.html")


tryme.run(debug=True)


"""                finances = db.session.query(Warehouse).filter(
                    Warehouse.finances == self.manager.account
                ).first()
                loghistory = History(
                    transaction="saldo", value=self.amount, comment=self.comment
                )
"""