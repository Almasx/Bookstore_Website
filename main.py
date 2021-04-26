import os
from datetime import *


from data.users import User
from flask import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from data import db_session, users_api
from data.db_session import create_session
from flask import make_response
from data.book import Book
from data.genre import Genre
from data.orders import Orders
from data.order_details import Order_details
from forms.forms import *
from requests import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
GENRE_LIST = ['Poetry', 'Fantasy', 'Science Fiction', 'Mystery', 'Biography', 'Drama']
db_session.global_init("db/library.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(users_api.blueprint)

@app.route("/")
@app.route("/index")
def index():
    session = create_session()
    books = [book.to_dict() for book in session.query(Book).all()]
    return render_template('catalog.html', title="Welcome to LMS", book_list=books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают')
            return render_template('register.html', title='Регистрация',
                                   form=form)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            flash("Такой пользователь уже есть")
            return render_template('register.html', title='Регистрация',
                                   form=form)
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.location = form.location.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        flash("Неправильный логин или пароль")
        return render_template('login.html',
                               form=form)
    return render_template('login.html', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        book = Book()
        book.author = current_user.id
        book.title = form.title.data
        book.about = form.about.data
        book.year = form.year.data
        book.genre_id = form.genre.data
        book.price = form.price.data
        filename = form.photo.data.filename
        form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        book.image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        session.add(book)
        session.commit()
        flash('Book successfully uploaded and displayed below')
        return redirect('/')
    return render_template('add_book.html', title='Adding a book',
                           form=form)


@app.route('/purchases', methods=['GET', 'POST'])
@login_required
def display_all_orders():
    json_file = get(f'http://localhost:5000/api/users/{str(current_user.id)}/purchase').json()
    if json_file != {'error': 'Not found'}:
        order, book, user, order_details, genre = json_file['order'], json_file['book'],\
                                                  json_file['user'], json_file['order_details'],\
                                                  json_file['genre']
        return render_template('purchases.html', title="Welcome to LMS",
                               orders=zip(book, genre, user, order, order_details))
    else:
        return render_template('purchases.html', title="Purchases",)


@app.route('/books/<int:book_id>', methods=['GET', 'POST'])
def order_book(book_id):
    form = AddOrderForm()
    if form.validate_on_submit():
        order_details = Order_details()
        order_details.order_date, order_details.shipment_date,\
        order_details.shipment_status = date.today(),\
                                        date.today() + timedelta(days=30), 'Not delivered'
        session = db_session.create_session()
        session.add(order_details)
        session.commit()
        order, session = Orders(), db_session.create_session()
        book = session.query(Book).get(book_id)
        order_details = session.query(Order_details).order_by(Order_details.id.desc()).first()
        order.book_id, order.user_id,\
        order.order_details_id = book_id, current_user.id, order_details.id
        order.amount, order.total_price = form.amount.data, form.amount.data * book.price
        session.add(order)
        session.commit()
        return redirect('/')
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    author = session.query(User).get(book.author)
    genre = session.query(Genre).get(book.genre_id)
    return render_template('view_book.html', title='Ordering a book',
                           form=form, book=book, author=author, genre=genre)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.errorhandler(401)
def redirect_login(error):
    return redirect(u'/login')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
