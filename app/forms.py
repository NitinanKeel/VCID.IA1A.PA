from ctypes.wintypes import SIZE
from select import select
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from app.models import User

# Form for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Form for registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    adminuser = BooleanField('Adminuser')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Form for adding budgets
class BudgetForm(FlaskForm):
    selectchoice = 'Spending','Income'
    description = StringField('Description', validators=[DataRequired()])
    choicefield = SelectField('Transaction Type', choices=selectchoice, validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for editing spending amount
class EditSpendingForm(FlaskForm):
    amount2 = IntegerField(validators=[DataRequired(), NumberRange(min=0)], render_kw={"placeholder": "spending limit"})
    submit2 = SubmitField('Edit')
