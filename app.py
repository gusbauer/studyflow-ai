from flask import Flask, render_template
from extensions import db
# from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash
from forms import RegisterForm
import models
from models import User

app = Flask(__name__)

app.config["SECRET_KEY"] = "studyflow-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studyflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# login_manager = LoginManager(app)
# login_manager.login_view = "login"


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")

        return redirect(url_for("index"))

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)