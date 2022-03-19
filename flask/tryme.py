from flask import Flask, render_template, request, redirect
from accountant_flask import create_manager

tryme = Flask(__name__)


@tryme.route("/", methods=["GET", "POST"])
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
