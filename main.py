from flask import Flask, render_template, redirect
from forms.user import *
from data import db_session
from data.__all_models import *
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "some_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def root():
    param = {
        'title': "Navigator in IT",
    }
    return render_template('base.html', **param)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    params = {
        'title': 'Регистрация',
        'form': form
    }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('users/register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('users/register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('users/register.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('users/login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('users/login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/db.db")
    app.run()


if __name__ == '__main__':
    main()
