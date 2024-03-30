import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #несколько вариантов хранить отдельно стартовую дату + обьект data.time.delay который будет временем брони или в формате 01.01.2000:02.01.2000
    description_to_order = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #мб системная инфа либо описание/предпочтение к заказу
