import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Hostel(SqlAlchemyBase):
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

    Parsing_dates = sqlalchemy.Column(sqlalchemy.String)

    #review  можно сделать отдельную таблицу под отзывы и сюда их id подключать?
