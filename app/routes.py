from flask import render_template, session, request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, AssetForm, TickerForm
from app.models import User, Asset, Ticker
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app.formatting import *
from app.functions import *
from app.update_ticker import *

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/asset_class', methods=['GET', 'POST'])
def asset():
    form = AssetForm()
    if request.method == 'POST':
        asset_class_name = request.form.get("asset_class_name")
        allocation_percent = request.form.get("allocation_percent")
        assets = Asset(asset_class_name=asset_class_name, allocation_percent=allocation_percent)
        db.session.add(assets)
        db.session.commit()
        return redirect(url_for('asset'))
    assets = Asset.query.order_by(Asset.asset_class_name)
    # this is a join.. the item in the join section is the left table
    return render_template('asset_class.html', form=form, assets=assets)


@app.route('/asset_update/<asset_class_id>/', methods=['GET', 'POST'])
def asset_update(asset_class_id):
    asset = Asset.query.get(asset_class_id)
    asset.asset_class_name = request.form.get("asset_class_name")
    asset.allocation_percent = request.form.get("allocation_percent")
    db.session.commit()
    flash(f"{asset.asset_class_name} has been updated.")
    return redirect(url_for('asset'))


@app.route('/asset_delete/<asset_class_id>/', methods=['GET', 'POST'])
def asset_delete(asset_class_id):
    db.session.query(Asset).filter(Asset.asset_class_id == asset_class_id).delete(synchronize_session='fetch')
    db.session.commit()
    flash(f"The asset class has been deleted.")
    return redirect(url_for('asset'))


@app.route('/tickers', methods=['GET', 'POST'])
def tickers():
    form = TickerForm()

    asset_classes = get_asset_classes()

    form.asset_classes.choices = [(asset_class['asset_class_id'], asset_class['asset_class_name']) for asset_class in asset_classes]

    if request.method == 'POST':
        ticker_symbol = request.form.get("ticker_symbol")
        company_name = request.form.get("company_name")
        #current_price = request.form.get("current_price")
        asset_class_id = request.form.get('asset_classes')
        ticker = Ticker(ticker_symbol=ticker_symbol, company_name=company_name, asset_classes=asset_classes)
        db.session.add(ticker)
        db.session.commit()
        return redirect(url_for('tickers'))
    tickers = get_tickers()
    # this is a join.. the item in the join section is the left table
    return render_template('tickers.html', form=form, asset_classes=asset_classes, tickers=tickers)

@app.route('/ticker_update/<ticker_id>/', methods=['GET', 'POST'])
def ticker_update(ticker_id):
    ticker = Ticker.query.get(ticker_id)
    ticker.ticker_symbol = request.form.get("ticker_symbol")
    ticker.company_name = request.form.get("company_name")
    ticker.asset_class_id = request.form.get("asset_class")
    db.session.commit()
    flash(f"The ticker has been updated.")
    return redirect(url_for('tickers'))

@app.route('/ticker_price_update', methods=['GET', 'POST'])
def ticker_price_update():
    post_ticker_prices()
    return redirect(url_for('tickers'))


@app.route('/ticker_delete/<ticker_id>/', methods=['GET', 'POST'])
def ticker_delete(ticker_id):
    db.session.query(Ticker).filter(Ticker.ticker_id == ticker_id).delete()
    db.session.commit()
    flash(f"The ticker has been deleted.")
    return redirect(url_for('tickers'))

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
