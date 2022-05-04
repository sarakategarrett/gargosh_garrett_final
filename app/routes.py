from flask import render_template, session, request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, AssetForm, TickerForm, BlogForm
from app.models import User, Asset, Ticker,  Blog
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
    assets = get_asset_classes()
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
        ticker = Ticker(ticker_symbol=ticker_symbol, company_name=company_name, asset_class_id=asset_class_id)
        db.session.add(ticker)
        db.session.commit()
        return redirect(url_for('tickers'))
    tickers = get_tickers()
    # this is a join.. the item in the join section is the left table
    return render_template('tickers.html', form=form, asset=asset, tickers=tickers)

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



@app.route('/blog')
def blog():
    form = BlogForm()
    if request.method == 'POST':
        blog_title = request.form.get("blog_title")
        blog_body = request.form.get("blog_body")
        blog_date = request.form.get("blog_date")
        blog_img = request.form.get("blog_img")
        blogs = Blog(blog_title=blog_title, blog_body=blog_body, blog_date=blog_date, blog_img=blog_img)
        db.session.add(blogs)
        db.session.commit()
        return redirect(url_for('blog'))
    blogs = Blog.query.order_by(Blog.blog_date.desc()).all()
    return render_template('blog.html', form=form, blogs=blogs)

@app.route('/blog_detail/<blog_id>/')
def blog_detail(blog_id):
    form = BlogForm()
    if request.method == 'POST':
        blog = Blog.query.get(blog_id)
        blog.blog_title = request.form.get("blog_title")
        blog.blog_body = request.form.get("blog_body")
        blog.blog_date = request.form.get("blog_date")
        blog.blog_img = request.form.get("blog_img")
        db.session.commit()
        return redirect(url_for('blog_detail'))
    blogs = Blog.query.order_by(Blog.blog_date.desc()).all()
    return render_template('blog_detail.html', form=form, blogs=blogs)

@app.route('/blog_view/<blog_id>/')
def blog_view(blog_id):
    form=BlogForm()
    if request.method == 'POST':
        blog = Blog.query.get(blog_id)
        blog.blog_title = request.form.get("blog_title")
        blog.blog_body = request.form.get("blog_body")
        blog.blog_date = request.form.get("blog_date")
        blog.blog_img = request.form.get("blog_img")
        db.session.commit()
        return redirect(url_for('blog'))
    blogs = Blog.query.order_by(Blog.blog_date.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.order_by(Blog.blog_date.desc()).paginate(page,
                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    return render_template('blog.html', blogs=blogs)
    blogs = pagination.items
    return render_template('blog.html', form=form, blogs=blogs, pagination=pagination)


@app.route('/blog_edit',  methods=['GET', 'POST'])
def blog_edit():
    form = BlogForm()
    if request.method == 'POST':
        blog_title = request.form.get("blog_title")
        blog_body = request.form.get("blog_body")
        blog_date = request.form.get("blog_date")
        blog_img = request.form.get("blog_img")
        blogs = Blog(blog_title=blog_title, blog_body=blog_body, blog_date=blog_date, blog_img=blog_img)
        db.session.add(blogs)
        db.session.commit()
        return redirect(url_for('blog_edit'))
    blogs = Blog.query.order_by(Blog.blog_date.desc()).all()
    return render_template('blog_edit.html', form=form, blogs=blogs)

@app.route('/blog_update/<blog_id>/', methods=['GET', 'POST'])
def blog_update(blog_id):
    blog = Blog.query.get(blog_id)
    blog.blog_title = request.form.get("blog_title")
    blog.blog_body = request.form.get("blog_body")
    blog.blog_date = request.form.get("blog_date")
    blog.blog_img = request.form.get("blog_img")
    db.session.commit()
    flash(f"{blog.blog_title} has been updated.")
    return redirect(url_for('blog_edit'))



@app.route('/blog_delete/<blog_id>/', methods=['GET', 'POST'])
def blog_delete(blog_id):
    db.session.query(Blog).filter(Blog.blog_id == blog_id).delete(synchronize_session='fetch')
    db.session.commit()
    flash(f"The Blog Post has been deleted.")
    return redirect(url_for('blog_edit'))




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





