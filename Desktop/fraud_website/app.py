from flask import Flask, render_template, request, redirect, session
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

users = {}
history = {}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user in users and users[user] == pwd:
            session["user"] = user
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Login")

    return render_template("login.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user in users:
            return render_template("signup.html", error="User exists")

        users[user] = pwd
        history[user] = []
        return redirect("/")

    return render_template("signup.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    result = None

    if request.method == "POST":
        try:
            values = pd.DataFrame([[
                float(request.form["amount"]),
                float(request.form["oldbalanceOrg"]),
                float(request.form["newbalanceOrig"]),
                float(request.form["oldbalanceDest"]),
                float(request.form["newbalanceDest"])
            ]], columns=[
                "amount",
                "oldbalanceOrg",
                "newbalanceOrig",
                "oldbalanceDest",
                "newbalanceDest"
            ])

            values = scaler.transform(values)
            pred = model.predict(values)[0]

            history[user].append((request.form["amount"], pred))

            if pred == 1:
                result = "Fraud 🚨"
            else:
                result = "Safe ✅"

        except:
            result = "Enter valid values"

    fraud_count = sum(1 for i in history[user] if i[1] == 1)
    safe_count = sum(1 for i in history[user] if i[1] == 0)

    total = fraud_count + safe_count

    if total > 0:
        fraud_percent = round((fraud_count / total) * 100, 2)
        safe_percent = round((safe_count / total) * 100, 2)
    else:
        fraud_percent = 0
        safe_percent = 0

    return render_template(
        "dashboard.html",
        result=result,
        data=history[user],
        fraud=fraud_percent,
        safe=safe_percent
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)