import sqlite3
import uuid
from datetime import datetime
from flask import render_template, flash, redirect, request, jsonify
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, BudgetForm, EditSpendingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Budget
from sqlalchemy import desc

# Index route
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# Dashboard route, accept GET and POST requests
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    current_userid = current_user.id
    spending_limit = current_user.spending_limit
    total_budget = 0
    monthy_income = 0
    monthy_spending = 0
    today = datetime.now()
    datem = datetime(today.year, today.month, 1)

    # Edit spending
    editspendingform = EditSpendingForm()
    if editspendingform.validate_on_submit():
        current_user.spending_limit = editspendingform.amount2.data
        db.session.commit()
        return redirect('dashboard')
    
    # Get budgets filter by User.ID
    budgets = Budget.query.filter_by(user_id=current_userid).order_by(desc(Budget.date))
    for budget in budgets:
        budgetdate = datetime(budget.date.year, budget.date.month, 1) 
        if budget.income != None:
            if datem == budgetdate:
                monthy_income += budget.income
            add_income = int(budget.income)
            total_budget += add_income
        if budget.spending != None:
            if datem == budgetdate:
                monthy_spending += budget.spending
            add_spending = int(budget.spending)
            total_budget -= add_spending
    
    # Form for adding budgets
    form = BudgetForm()
    spending_amount = None
    income_amount = None
    if form.validate_on_submit():
        if form.choicefield.data == "Spending":
            spending_amount = form.amount.data
        elif form.choicefield.data == "Income":
            income_amount = form.amount.data
        user = Budget(user_id=current_user.get_id(), description=form.description.data, spending=spending_amount, income=income_amount, date=form.date.data)
        db.session.add(user)
        db.session.commit()
        return redirect('dashboard')
    
    return render_template('dashboard.html', form=form, editspendingform=editspendingform, budgets=budgets, income=monthy_income, spending=monthy_spending, total_budget=total_budget, spending_limit=spending_limit)

# Account route
@app.route('/account')
@login_required
def account():
    return render_template('account.html', current_user=current_user)

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('index')
    
    # Init Registrationform
    form = RegistrationForm()
    
    # Validate input
    if form.validate_on_submit():
        
        # Create User with api_key
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, adminuser=form.adminuser.data, api_key=uuid.uuid4().hex)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('login')
    return render_template('signup.html', title='SignUp', form=form)

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)

        # Redirect to next page after login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = 'index'
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')

# Delete budget entries with budget id from database
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    entry_to_delete = Budget.query.get_or_404(id)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash("Entry deleted successfully!")
    except:
        flash("Error deleting entry")
    return redirect('/dashboard')

# API Route get user and budget from database as JSON
@app.route('/api/users')
def api_getusers():
    headers = request.headers
    auth = headers.get('X-Api-Key')
    user = User.query.filter_by(api_key=auth).first()
    if user:
        # If User is admin get all entries from all users
        if user.adminuser == True:
            user = User.query.all()
            return jsonify(user), 200
        else:
            # Else only return user specific budget data
            return jsonify(user), 200
    else:
        return jsonify({"message": "Error"}), 401

