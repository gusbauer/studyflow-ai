from flask import Flask, render_template, redirect, url_for, flash, request

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from extensions import db, login_manager

from forms import RegisterForm, LoginForm, TaskForm

import models
from models import User, Task
app = Flask(__name__)

app.config["SECRET_KEY"] = "studyflow-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studyflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager.init_app(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            flash("Welcome back!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
@app.route("/task/new", methods=["GET", "POST"])
@login_required
def new_task():

    form = TaskForm()

    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task created successfully!", "success")

        return redirect(url_for("dashboard"))

    return render_template("create_task.html", form=form)
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("login"))