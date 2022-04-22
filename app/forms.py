from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AssetForm(FlaskForm):
    asset_class_name = StringField('Asset Name', validators=[DataRequired()])
    allocation_percent = StringField('Allocation Percentage', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TickerForm(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    asset_classes = SelectField('Asset Class', choices=[])
    submit = SubmitField('Submit')


