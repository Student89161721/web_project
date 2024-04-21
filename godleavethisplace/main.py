from flask import Flask, render_template, redirect, make_response, session, request, abort, url_for
import sqlalchemy
import datetime
from data import db_session, hostel_api
from data.users import User, LoginForm, RegisterForm
from data.hostels import Hostel
from data.orders import Order
import sqlalchemy_serializer
from flask import jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from forms.user import RegisterForm
from forms.hostels import HostelsForm



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
    if not current_user.is_authenticated:
        return render_template('index.html', **param)
    else:
        return redirect('/hostels/page/1')


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
    content = db_sess.query(Hostel).filter(Hostel.id <= 10 * page_num, 10 * (page_num - 1) <= Hostel.id).all()
    return render_template('hostels.html', content=content, page_num=page_num)

@app.route('/hostels/current/<int:hostel_id>', methods=['GET', 'POST'])
def hostels_current(hostel_id):
    global sp, content
    err = ''
    db_sess = db_session.create_session()
    print(hostel_id, type(hostel_id))
    if hostel_id == 0:
        hostel_id = content.id
        user_id = current_user.id
        order = Order()
        order.hostel_info = content.id
        order.user_info = current_user.id


        asv = request.form['calendar']
        order.description = request.form['comment']
        print(asv)
        if asv != '':
            order = Order()
            order.hostel_info = content.id
            order.user_info = current_user.id

            order.description = request.form['comment']

            date_strings = asv.split('-')
            date_strings = (datetime.date(day=int(date_strings[-1]), month=int(date_strings[1]),
                                                     year=int(date_strings[0])))
            print((date_strings - datetime.date.today()).days)
            if (date_strings - datetime.date.today()).days < 0:
                err = 'данные ошибочны'
            print(date_strings)
            order.date_info = date_strings
            db_sess.merge(order)
            db_sess.commit()

        else:
            err = 'данные ошибочны'
        #return render_template('tester.html', sp=sp)
        #тут данные заказа вставлять
    content = db_sess.query(Hostel).filter(Hostel.id == hostel_id).first()
    sp = content.to_dict()
    print(sp, 'fitst')
    return render_template('current_hostel.html', content=content, sp=sp, err=err)

@app.route('/hostels/edit/<int:hostel_id>',  methods=['GET', 'POST'])
@login_required
def add_news(hostel_id):
    form = HostelsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        hostel = Hostel()
        #тут нужно из hostel_edit поставить приколы
        hostel.Title = 'ТЕСТОВАЯ ПОПЫТКА'
        hostel.Email = 'test@email.ru'
        hostel.Region = 'ТЕСТОВЫЙ РЕГИОН'
        hostel.Parsing_dates = 'ТЕСТОВАЯ ШТУКА'

        db_sess.merge(hostel)
        db_sess.commit()
        return redirect('/')
    return render_template('hostels_edit.html', title='Добавление новости',
                           form=form)

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_current(user_id):
    db_sess = db_session.create_session()
    print(current_user.id)
    order = db_sess.query(Order).filter(Order.user_info == user_id)
    content = db_sess.query(User).filter(User.id == user_id).first()
    if current_user.is_authenticated and current_user.id == user_id:
        return render_template('account.html', content=content, id=id, order=order, date=datetime.date.today())
    else:
        return 'Пользователь не найден'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request():
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
