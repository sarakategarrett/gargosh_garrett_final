from flask import render_template, session, request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, AssetForm
from app.models import User, Asset
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app.formatting import *

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    form_username = form.username.data
    form_password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=form_username).first()
        password = user.password
        if user is None or password != form_password:
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        session.permanent = True
        return redirect(url_for("home"))
    return render_template("login.html", title="Sign In", form=form)


@app.route('/asset', methods=['GET', 'POST'])
def asset():
    form = AssetForm()
    if request.method == 'POST':
        name = request.form.get("name")
        date = request.form.get("date")
        assets = Asset(name=name, date=date)
        db.session.add(assets)
        db.session.commit()
        return redirect(url_for('asset'))
    assets = Asset.query.order_by(Asset.name)
    # this is a join.. the item in the join section is the left table
    return render_template('asset_class.html', form=form, assets=assets)


@app.route('/asset_update/<id>/', methods=['GET', 'POST'])
def asset_update(id):
    asset = Asset.query.get(id)
    asset.name = request.form.get("name")
    asset.date = request.form.get("date")
    db.session.commit()
    flash(f"{asset.name} has been updated.")
    return redirect(url_for('asset'))


@app.route('/asset_delete/<id>/', methods=['GET', 'POST'])
def asset_delete(id):
    db.session.query(Asset).filter(Asset.id == id).delete()
    db.session.commit()
    flash(f"The asset class has been deleted.")
    return redirect(url_for('asset'))


@app.route('/tickers')
def tickers():
    return render_template("tickers.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
