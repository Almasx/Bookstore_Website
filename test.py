import flask
from flask import jsonify, request

from data import db_session
from data.users import User
from data.book import Book
from data.orders import Orders
from data.genre import Genre
from data.order_details import Order_details

db_session.global_init("db/library.sqlite")
session = db_session.create_session()
orders = session.query(Orders).filter(Orders.user_id == 1).all()
if not orders:
    print(1)