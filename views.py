from .app import app
from flask import redirect, render_template, url_for
from .models import get_sample
from .models import *
from wtforms import PasswordField
from .models import User
from hashlib import sha256
from flask_login import login_user , current_user
from flask import request
from flask_login import login_required

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class AuthorForm (FlaskForm):
    id = HiddenField ('id')
    name = StringField ('Nom', validators =[DataRequired()])

"""
@app.route("/")
def home():
    return render_template(
        "home.html",
        title="Hello World!",
        names=["Pierre","Paul","Corinne"])
    """
@app.route("/")
def home():
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample())

@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)]
    return render_template("detail.html",b=book)

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm (id=a.id, name=a.name)
    return render_template(
        "edit-authors.html",
        author =a, form=f)

@app.route("/save/author/", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('edit_author', id=a.id))
    a = get_author(int(f.id.data))
    return render_template ("edit-author.html",
    author=a, form=f)

    
    
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None


@app.route("/login/", methods =("GET","POST" ,))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect( url_for("home"))
    return render_template(
    "login.html",
    form=f)

from flask_login import logout_user
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))