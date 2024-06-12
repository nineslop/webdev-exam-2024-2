from flask import render_template, redirect, url_for, request, flash, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_login import login_user, current_user, login_required, LoginManager, logout_user
from models import db
from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember_me'))

        user = db.session.query(User).filter_by(login=login).scalar()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', current_user=current_user)

def load_user(user_id):
    return db.session.query(User).filter(User.id == int(user_id)).one()


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def check_perm(rule):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Необходимо войти в систему для доступа к данной странице.', 'warning')
                return redirect(url_for('login'))
            if not current_user.can(rule):
                flash('У вас нет прав доступа к данной странице.', 'warning')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator