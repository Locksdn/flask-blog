from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_login.utils import login_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from .app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/login')
def login():
    return render_template('login.html')

@admin.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('admin.dashboard'))
    
    flash('INVALID LOGIN')
    return redirect(url_for('admin.login'))

@admin.route('/signup')
def signup():
    return render_template('singup.html')

@admin.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    password = request.form.get('password')

    user = User(name, generate_password_hash(password))

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('admin.login'))

@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))

@admin.route('/')
@login_required
def dashboard():
    return render_template('admin_dashboard.html')

@admin.route('/<entry_id>/edit')
@login_required
def entry_edit(entry_id):
    return render_template('edit_entry.html')

@admin.route('/new')
@login_required
def new_entry():
    return render_template('new_entry.html')