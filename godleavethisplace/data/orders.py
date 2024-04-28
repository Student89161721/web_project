import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_info = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),  nullable=False)
    hostel_info = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date_info = sqlalchemy.Column(sqlalchemy.Date)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.String, default=str(datetime.date.today()))

