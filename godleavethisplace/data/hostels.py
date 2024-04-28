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


class Hostel(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'hostel'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    Websites = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Title = sqlalchemy.Column(sqlalchemy.String)

    Description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Cell_phones = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Landline_phones = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    Email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)

    Region = sqlalchemy.Column(sqlalchemy.String)
    Locality = sqlalchemy.Column(sqlalchemy.String, unique=True)

    VK = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Instagram = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Facebook = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    WhatsApp = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Viber = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    YouTube = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Telegram = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Twitter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    master_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    #review  можно сделать отдельную таблицу под отзывы и сюда их id подключать?

class HostelsForm(FlaskForm):
    #мне лень тут расписывать. Сделайте ппжпж
    Websites = StringField('Сайты', validators=[DataRequired()])
    Title = StringField('Заголовок', validators=[DataRequired()])
    Description = StringField('Описание', validators=[DataRequired()])
    Cell_phones = StringField('Сотовые телефоны', validators=[DataRequired()])
    Landline_phones = StringField('Городские телефоны', validators=[DataRequired()])
    Email = StringField('Электронная почта', validators=[DataRequired()])
    Region = StringField('Регион', validators=[DataRequired()])
    Locality = StringField('Локация', validators=[DataRequired()])
    VK = StringField('VK', validators=[DataRequired()])
    Instagram = StringField('Instagram', validators=[DataRequired()])
    Facebook = StringField('Facebook', validators=[DataRequired()])
    WhatsApp = StringField('WhatsApp', validators=[DataRequired()])
    Viber = StringField('Viber', validators=[DataRequired()])
    YouTube = StringField('YouTube', validators=[DataRequired()])
    Telegram = StringField('Telegram', validators=[DataRequired()])
    Twitter = StringField('Twitter', validators=[DataRequired()])
    submit = SubmitField('Применить')