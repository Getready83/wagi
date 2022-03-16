from flask import Flask, render_template, request, redirect

tryme = Flask(__name__)


@tryme.route("/")
def hello():
    return render_template(
        "accountant.html"
    )

@tryme.route("/history/")
def hello2():
    return render_template(
        "history.html"
    )

@tryme.route("/test/", methods=["GET", "POST"])
def hello1():
    firstname = request.args.get("firstname")
    email = request.args.get("email")
    department = request.args.get("departments")
    return render_template(
        "index1.html", firstname=firstname, email=email, department=department
    )


@tryme.route("/form/", methods=["POST"])
def hello_formularz():
    firstname = request.args.get("firstname", "")
    email = request.args.get("email", "")
    department = request.args.get("departments", "")
    return redirect("/")


tryme.run(debug=True)
