from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

USER = {
    "username": "admin",
    "password": "123456"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form["username"] == USER["username"] and
            request.form["password"] == USER["password"]):
            session["user"] = USER["username"]
            return redirect(url_for("age"))
        else:
            return render_template("login.html", error="Sai tài khoản hoặc mật khẩu")
    return render_template("login.html")

@app.route("/age", methods=["GET", "POST"])
def age():
    if "user" not in session:
        return redirect(url_for("login"))

    age = None
    if request.method == "POST":
        dob = datetime.strptime(request.form["dob"], "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

    return render_template("age.html", age=age)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
