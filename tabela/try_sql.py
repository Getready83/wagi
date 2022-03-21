from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sql import create_manager


try_sql = Flask(__name__)
try_sql.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(try_sql)

class Saldo(db.Model):
    current_acountent_state = db.Column(db.Float)


class Warehouse(db.Model):
    product_name = db.Column(db.String(30), primary_key=True)
    product_quantity = db.Column(db.Integer)


class History(db.Model):



@try_sql.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.main_loop()
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


@try_sql.route("/history/", methods=["GET", "POST"])
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


@try_sql.route("/thanks/", methods=["Get", "POST"])
def thankyou():
    return render_template("thanks.html")


try_sql.run(debug=True)
