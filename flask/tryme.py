import sys
from flask import Flask, render_template, request, redirect
from accountant_flask import create_manager
tryme = Flask(__name__)


@tryme.route("/", methods=["GET", "POST"])
def hello():
    manager, action_type = create_manager()
    account = manager.main_loop()
    warehouse = manager.warehouse
    action = request.form.get("action")
    if action in action_type:
        manager.execute(action)
    name = request.form.get("name")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    return render_template(
        "accountant.html", name=name, price=price, quantity=quantity,
        manager=manager, account=account, warehouse=warehouse
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

@tryme.route("/test/", methods=["GET", "POST"])
def hello1():
    name = request.args.get("name")
    price = request.args.get("price")
    quantity = request.args.get("quantity")
    return render_template(
        "index1.html", name=name, price=price, quantity=quantity
    )


@tryme.route("/form/", methods=["POST"])
def hello_formularz():
    name = request.args.get("name", "")
    price = request.args.get("price", "")
    quantity = request.args.get("quantity", "")
    return redirect("/")

@tryme.route("/thanks/")
def thankyou():
    print("thank you")
    return redirect("/")


tryme.run(debug=True)
