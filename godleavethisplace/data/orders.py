import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    hotel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hotels.id"))

    #day_start =
    #несколько вариантов хранить отдельно стартовую дату + обьект data.time.delay который будет временем брони или в формате 01.01.2000:02.01.2000
    description_to_order = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #мб системная инфа либо описание/предпочтение к заказу
