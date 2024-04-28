import datetime
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    #name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #несколько вариантов хранить отдельно стартовую дату + обьект data.time.delay который будет временем брони или в формате 01.01.2000:02.01.2000
    user_info = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),  nullable=False)
    hostel_info = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date_info = sqlalchemy.Column(sqlalchemy.Date)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #мб системная инфа либо описание/предпочтение к заказу
    created_date = sqlalchemy.Column(sqlalchemy.String, default=str(datetime.date.today()))


