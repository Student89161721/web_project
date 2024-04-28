from flask import Flask, render_template, redirect, make_response, session, request, abort, url_for
import sqlalchemy
import datetime
from data import db_session, hostel_api
from data.users import User, LoginForm, RegisterForm
from data.hostels import Hostel, HostelsForm
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
    param = {'title': 'Домашняя страница'}
    if not current_user.is_authenticated:
        return render_template('index.html', **param)
    else:
        if current_user.is_master == 1:
            return redirect('/hostels/page/1')
        else:
            return redirect(f'/user/{current_user.id}')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
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
        v = request.form['contact']
        if v == 'email':
            user.is_master = 1
        else:
            user.is_master = 2
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/hostels/page/<int:page_num>', methods=['GET', 'POST'])
def hostels(page_num):
    global h_filter
    db_sess = db_session.create_session()
    if h_filter is None:
        cont = db_sess.query(Hostel).filter(Hostel.id <= 10 * page_num, 10 * (page_num - 1) <= Hostel.id).all()
    else:
        cont = (db_sess.query(Hostel).filter(Hostel.Region == h_filter).all
                ())
    if request.method == "POST":
        h_filter = request.form.getlist('year[]')[0]

    return render_template('hostels.html', content=cont, page_num=page_num, alt_h=alt_h)


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
    content = db_sess.query(Hostel).filter(Hostel.id == hostel_id).first()
    sp = content.to_dict()
    print(sp, 'fitst')
    return render_template('current_hostel.html', content=content, sp=sp, err=err)


@app.route('/hostels/add',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = HostelsForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        hostel = Hostel()

        hostel.Title = form.Title.data
        hostel.Email = form.Email.data
        hostel.Region = form.Region.data
        hostel.Websites = form.Websites.data
        hostel.Cell_phones = form.Cell_phones.data
        hostel.Description = form.Description.data
        hostel.Facebook = form.Facebook.data
        hostel.VK = form.VK.data
        hostel.Viber = form.Viber.data
        hostel.WhatsApp = form.WhatsApp.data
        hostel.master_id = current_user.id

        db_sess.add(hostel)
        db_sess.commit()
        return redirect('/')
    return render_template('hostels_add.html', form=form)

@app.route('/hostels/del/<int:hostel_id>',  methods=['GET', 'POST'])
@login_required
def del_hostel(hostel_id):
    db_sess = db_session.create_session()
    hostel = db_sess.query(Hostel).filter(Hostel.id == hostel_id).all()[0]
    print(hostel)
    db_sess.delete(hostel)
    db_sess.commit()
    return redirect('/')



@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_current(user_id):
    db_sess = db_session.create_session()
    print(current_user.id)
    order = db_sess.query(Order).filter(Order.user_info == user_id)
    cont = db_sess.query(User).filter(User.id == user_id).first()
    trust = db_sess.query(Hostel).filter(Hostel.master_id == user_id).all()
    print(order, trust)
    [print(i.id) for i in trust]
    if current_user.is_authenticated and current_user.id == user_id:
        return render_template('account.html', content=cont, id=user_id, order=order,
                               date=datetime.date.today(), ismaster=str(current_user.is_master), hostels=trust)
    else:
        return 'Пользователь не найден'


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    global alt_h
    db_session.global_init("db/data2.sqlite")
    app.register_blueprint(hostel_api.blueprint)
    db_sess = db_session.create_session()
    alt_h = list(set([i.Region for i in db_sess.query(Hostel).all()]))[1:]
    alt_h = list(filter(lambda x: len(str(x)) > 4, alt_h))
    db_sess.close()
    app.run()

h_filter = None
if __name__ == '__main__':
    main()
