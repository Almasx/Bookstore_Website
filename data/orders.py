import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Orders(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_details_id = sqlalchemy.Column(sqlalchemy.Integer,
                                         sqlalchemy.ForeignKey("order_details.id"))
    book_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("books.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    amount = sqlalchemy.Column(sqlalchemy.Integer)
    total_price = sqlalchemy.Column(sqlalchemy.Integer)
    user, book = orm.relation('User'), orm.relation('Book')
    order_details = orm.relation('Order_details')