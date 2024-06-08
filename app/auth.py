from flask import render_template, redirect, url_for, request, flash
from functools import wraps
from flask_login import login_user, current_user, login_required, LoginManager, logout_user
from app import app, db
from .models import User
from .forms import LoginForm

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(login=login).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.', 'danger')

    return render_template('login.html', form=form, current_user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in roles:
                return func(*args, **kwargs)
            else:
                flash('У вас недостаточно прав для выполнения данного действия', 'error')
                return redirect(url_for('index'))
        return decorated_view
    return wrapper

def custom_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для выполнения данного действия необходимо пройти процедуру аутентификации', 'error')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view

@app.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/moderator')
@role_required('moderator')
def moderator_dashboard():
    return render_template('moderator_dashboard.html')
