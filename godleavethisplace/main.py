from flask import Flask, render_template, redirect, make_response, session, request, abort, url_for
import sqlalchemy
from data import db_session, hostel_api
from data.users import User, LoginForm, RegisterForm
from data.hostels import Hostel
import sqlalchemy_serializer
from flask import jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)



@app.route('/', methods=['GET', 'POST'])
def index():
    param = {}
    param['title'] = 'Домашняя страница'
    return render_template('index.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',message="Неправильный логин или пароль",form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
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
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/hostels/page/<int:page_num>', methods=['GET', 'POST'])
def hostels(page_num):
    db_sess = db_session.create_session()
    db_sess = db_session.create_session()
    content = db_sess.query(Hostel).filter(10 * (page_num - 1) <= Hostel.id <= 10 * page_num).all()
    return render_template('hostels.html', page_num=[i.id for i in content])

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

def main():
    db_session.global_init("db/data2.sqlite")
    #hostel = Hostel()
    #hostel.Title = "ТЕСТ"
    #hostel.Email = "TEST@mail.ru"
    #hostel.Region = 'TEST REG'
    #hostel.Parsing_dates = '123'
    #db_sess = db_session.create_session()
    #db_sess.add(hostel)
    #db_sess.commit()
    app.register_blueprint(hostel_api.blueprint)
    app.run()
    #db_session.global_init("db/data2.sqlite")


if __name__ == '__main__':
    main()
