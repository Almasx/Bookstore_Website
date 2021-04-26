import flask
from flask import jsonify, request

from data import db_session
from data.users import User
from data.book import Book
from data.orders import Orders
from data.genre import Genre
from data.order_details import Order_details

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict() for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict()
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'location', 'books_written', 'email']):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    users = session.query(User).filter(User.id == user_id).first()
    if users is None:
        return jsonify({'error': 'Id does not exists'})

    users.name = request.json['name']
    users.surname = request.json['surname']
    users.location = request.json['location']
    users.books_written = request.json['books_written']
    users.email = request.json['email']
    session.commit()
    return jsonify({"success": "OK"})


@blueprint.route('/api/books/genre/<int:genre_id>', methods=['GET'])
def filter_by_genre(genre_id):
    session = db_session.create_session()
    books = session.query(Book).filter(Book.genre_id == genre_id).all()
    if not books:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "books": [book.to_dict() for book in books]
        }
    )


@blueprint.route('/api/users/<int:user_id>/purchase', methods=['GET'])
def get_users_purchase(user_id):
    session = db_session.create_session()
    orders = session.query(Orders).filter(Orders.user_id == user_id).all()
    if not orders:
        return jsonify({'error': 'Not found'})

    return jsonify({
        'order': [order.to_dict(only=('total_price', 'amount')) for order in orders],
        'book': [session.query(Book).get(order.book_id).to_dict(only=('id', 'title', 'year'))
                 for order in orders],
        'genre': [session.query(Genre).get(session.query(Book).get(order.book_id).genre_id).to_dict(only=('name',))
                  for order in orders],
        'user': [session.query(User).get(order.user_id).to_dict(only=('name', 'surname'))
                 for order in orders],
        'order_details': [session.query(Order_details).get(
            order.order_details_id).to_dict(only=('order_date', 'shipment_date', 'shipment_status'))
                          for order in orders]
        })
