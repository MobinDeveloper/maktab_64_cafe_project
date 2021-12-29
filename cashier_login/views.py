from flask import Flask, render_template, url_for, session, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "FLASK_DJANGO"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://backdoor:123456789@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)


def login_page():
    if request.method == "GET":
        return render_template("login_page.html")
    else:
        username = request.values.get("username")
        password = request.values.get("password")
        if check_data(username, password):
            session["username"] = username
            session["password"] = password
            return render_template("home_page.html",
                                   data={"username": session["username"], "password": session["password"],
                                         "navs": ["HOME", "MENU", "ABOUT", "LOGOUT"]})
        else:
            return render_template("login_page.html")


def register_page():
    if request.method == "GET":
        return render_template("register_page.html")
    else:
        username = request.values.get("username")
        password = request.values.get("password")
        fullname = request.values.get("fullname")
        if register(fullname, username, password):
            return render_template("login_page.html")
        else:
            return render_template("register_page.html")


########################################################db_part#########################################################
def check_data(username, password):
    real_password = User.query.filter_by(username=username).first().password
    if password == real_password:
        return True
    else:
        return False


def register(fullname, username, password):
    db.session.add(User(fullname=fullname, username=username, password=password))
    db.session.commit()
    return True


def log_out(username):
    User.query.filter_by(username=username).delete()
    db.session.commit()
    return True


# register("mobin atashi", "phoenix2", "mobin1234")
# print(log_out("Flask"))
# check_data("phoenix", "mobin1hbhjeav")
