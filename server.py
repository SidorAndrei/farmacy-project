from flask import Flask, render_template, redirect, url_for, request, session

import cryptography
import database_manager

# import dotenv
# dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = b'_5#87x"F4Qdu\n\xec]/'


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user = database_manager.get_user(request.form["username"])
        if cryptography.verify_password(request.form["password"], user["password"]):
            session.update({"username": user["username"], "user_id": user["ID_user"]})
            print("connection ok")
            return redirect(url_for("main_page"))
    return render_template("login_page.html")


# LOGOUT PAGE
@app.route("/logout")
def logout_page():
    session.pop("username")
    session.pop("user_id")
    return redirect(url_for("main_page"))


# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        password = request.form.get("reg_password")
        confirm_password = request.form.get("reg_password_confirm")
        if password == confirm_password:
            database_manager.insert_user(
                username=request.form.get("reg_username"),
                password=cryptography.hash_password(password),
            )
            return redirect(url_for("login_page"))
    return render_template("register_page.html")


@app.route('/')
def main_page():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('base_template.html', username=session["username"], user_id=session["user_id"])


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
