import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Order_details(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order_details'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_date = sqlalchemy.Column(sqlalchemy.Date)
    shipment_date = sqlalchemy.Column(sqlalchemy.String)
    shipment_status = sqlalchemy.Column(sqlalchemy.String)