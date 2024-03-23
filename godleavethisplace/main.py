from flask import Flask, render_template, redirect, make_response, session, request, abort, url_for
import sqlalchemy
from data import db_session
from data.users import User
from data.hostels import Hostel
import sqlalchemy_serializer
from flask import jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField




app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    param = {}
    param['username'] = "Ученик Яндекс.Лицея"
    param['title'] = 'Домашняя страница'
    return render_template('index.html', **param)
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
    #app.run()
    #db_session.global_init("db/data2.sqlite")




if __name__ == '__main__':
    main()
