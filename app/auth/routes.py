from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # страница входа в систему
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # ищет пользователя по имени
        user = User.query.filter_by(username=form.username.data).first()
        # проверяет пароль
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Вход', form=form)


@bp.route('/register', methods=['GET', 'POST'])
# страница регистрации
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация завершена! Теперь вы можете войти.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/logout')
def logout():
    # выход из системы
    logout_user()
    return redirect(url_for('main.index'))
