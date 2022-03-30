from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def get_id(self):
        return (self.id)

class Asset(db.Model):
    asset_class_id = db.Column(db.Integer, primary_key=True)
    asset_class_name = db.Column(db.String(166))
    allocation_percent = db.Column(db.Float)
    tickers = db.relationship('Ticker', backref='tickers', lazy=True)


class Ticker(db.Model):
    ticker_id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(166))
    company_name = db.Column(db.String(166))
    current_price = db.Column(db.String(166))
    asset_class_id = db.Column(db.Integer, db.ForeignKey('asset.asset_class_id'), nullable=False)

