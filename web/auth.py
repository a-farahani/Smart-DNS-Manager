from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize the blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Flask login setup
login_manager = LoginManager()

# Get username and password from environment variables
USERNAME = os.getenv('FLASK_USERNAME', 'admin')  # Default username
PASSWORD = os.getenv('FLASK_PASSWORD', 'password')  # Default password
hashed_password = generate_password_hash(PASSWORD)  # Hash once when the app starts

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username) if username == USERNAME else None

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and check_password_hash(hashed_password, password):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))  # Redirect to the main page after login
        flash('Invalid username or password')
    return render_template('login.html')

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Initialize login manager
def init_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect users to the login page if not authenticated
