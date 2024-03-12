from WEB_YL.data.utils import logout_required, confirm_token, generate_token
from flask import redirect, url_for, render_template, Blueprint
from WEB_YL.data import db_session
from WEB_YL.forms.user import LoginForm, RegisterForm, AskRecoveryForm, AcceptRecoveryForm, RecoveryForm
from WEB_YL.data.__all_models import User
from flask_login import login_required, login_user, logout_user, current_user
from flask import current_app as app
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

blueprint = Blueprint('users', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    reg_form = RegisterForm()
    log_form = LoginForm()
    params = {
        'title': 'Регистрация',
        'reg_form': reg_form,
        'log_form': log_form
    }
    if log_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == log_form.email.data).first()
        if user and user.check_password(log_form.password.data):
            login_user(user, remember=log_form.remember_me.data)
            return redirect("/")
        params['message'] = "Неправильный логин или пароль"
        # return render_template('users/login.html', **params)
    if reg_form.validate_on_submit():
        if reg_form.password.data != reg_form.password_again.data:
            params['message'] = "Пароли не совпадают"
            return render_template('users/login.html', **params)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == reg_form.email.data).first():
            params['message'] = "Такой пользователь уже есть"
            return render_template('users/login.html', **params)
        user = User(
            name=reg_form.name.data,
            email=reg_form.email.data
        )
        user.set_password(reg_form.password.data)
        db_sess.add(user)
        db_sess.commit()
        with app.app_context():
            token = generate_token(user.email)
            confirm_url = url_for("users.confirm_email", token=token, _external=True)
            template = render_template("users/confirm_email.html", confirm_url=confirm_url)
            msg = MIMEMultipart()
            msg['Subject'] = Header('Subject of the email', 'utf-8')
            msg.attach(MIMEText(template.encode('utf-8'), 'html', 'utf-8'))
            server = SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(app.config['MAIL_DEFAULT_SENDER'], app.config['MAIL_PASSWORD'])
            server.sendmail(app.config['MAIL_USERNAME'], user.email, msg.as_string())
            server.close()
        login_user(user)
        return redirect('/')
    return render_template('users/login.html', **params)


@blueprint.route("/confirm/<token>")
@login_required
def confirm_email(token):
    params = {
        'title': 'Подтверждение аккаунта',
        'message': str()
    }
    if current_user.is_confirmed:
        params['message'] = "Аккаунт уже подтверждён"
        return render_template('users/account_confirm.html', **params)
    db_sess = db_session.create_session()
    email = confirm_token(token)
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    if user:
        if user.email == email:
            current_user.is_confirmed = True
            db_sess.merge(current_user)
            db_sess.commit()
            params['message'] = "Аккаунт успешно подтверждён"
            return render_template('users/account_confirm.html', **params)
        else:
            params['message'] = "Ссылка недействительна"
            return render_template('users/account_confirm.html', **params)
    else:
        params['message'] = "Пользователь не найден"
        return render_template('users/account_confirm.html', **params)


@blueprint.route("/recovery_account", methods=['GET', 'POST'])
def recovery_account():
    form = AskRecoveryForm()
    params = {
        'form': form
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            with app.app_context():
                token = generate_token(user.email)
                confirm_url = url_for("users.recovery_email", token=token, _external=True)
                template = render_template("users/recovery_email.html", confirm_url=confirm_url)
                msg = MIMEMultipart()
                msg['Subject'] = Header('Subject of the email', 'utf-8')
                msg.attach(MIMEText(template.encode('utf-8'), 'html', 'utf-8'))
                server = SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(app.config['MAIL_DEFAULT_SENDER'], app.config['MAIL_PASSWORD'])
                server.sendmail(app.config['MAIL_USERNAME'], user.email, msg.as_string())
                server.close()
                params['message'] = "Вам на почту отправлено письмо с инструкцией по восстановлению аккаунта"
        else:
            params['message'] = "Пользователя с такой почтой не существует"
    return render_template('users/recovery_account.html', **params)


@blueprint.route("/recovery/<token>")
@login_required
def confirm_email(token):
    params = {
        'form': RecoveryForm(),
        'message': str()
    }
    db_sess = db_session.create_session()
    email = confirm_token(token)
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    if params['form'].validate_on_submit() and params['form'].password == params['form'].password_again:
        if user:
            if user.email == email:
                user.set_password(params['form'].password)
                db_sess.commit()
                params['message'] = "Аккаунт успешно подтверждён"
                login_user(user)
                return redirect("/")
            else:
                params['message'] = "Ссылка недействительна"
                return render_template('users/recovery_account.html', **params)
        else:
            params['message'] = "Пользователь не найден"
            return render_template('users/recovery_account.html', **params)
    params['message'] = "Пароли не совпадают"
    return render_template('users/recovery_account.html', **params)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/profile/<int:id>')
def profile(id: int):
    pass
