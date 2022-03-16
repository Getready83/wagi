from flask import Flask, render_template, request, redirect

accountant = Flask(__name__)

@accountant.route("/")
def home():
    magazyn = {"chleb": 3, "maslo": 2, "ser": 1}
    return render_template("index.html" ,magazyn=magazyn)



#@accountant.route("/zakup.html", methods=["GET","POST"])
#def form_buy():



accountant.run(debug=True)

#app.run()