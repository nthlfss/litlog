"""

This handles all the routes for the site
Here we can control how users will move between
pages, and set parameters that restrict or
allow access

"""

from flask import render_template, url_for, flash, redirect, request, abort
from litlog.forms import RegistrationForm, LoginForm, UpdateProfileForm, ReviewForm, SearchForm
from litlog.models import User, Book
from litlog import app, db, bcrypt
import secrets
import os
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
from apiclient.discovery import build


# The front page of the site. First thing users will see
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', books=books)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already logged in go to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # Check if data entered by user matches data in User table
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Take user to page they were headed to before logging in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        # If incorrect info entered, flash error message
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout option redirects to home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    # If user already logged in go to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Pass info into their respective columns
        user = User(username=form.username.data, first=form.first.data, last=form.last.data, email=form.email.data, password=hashed_password)
        # And save info in User table
        db.session.add(user)
        db.session.commit()
        flash(f'profile created for {form.username.data}!', 'success')
        # Once succesfully registered, take user to login page
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Defines a function to handle saving profile pictures uploaded by users
def save(form_picture):
    # Save random number in variable to be used as filename
    random = secrets.token_hex(8)
    # Split the pathname path into a pair (root, ext)
    _, f_ext = os.path.splitext(form_picture.filename)
    # Save in variable the random number with the ext to create new name for image uploaded (don't keep the orig filename)
    p_filename = random + f_ext
    # Folder where pictures are saved
    p_path = os.path.join(app.root_path, 'static/pics', p_filename)
    # Set size for all uploaded pictures
    size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(size)
    i.save(p_path)
    return p_filename

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first()
    books = Book.query.filter_by(writer=user).order_by(Book.date_posted.desc()).paginate(page=page)
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('profile.html', title='profile', image_file=image_file, books=books, user=user, form=form)

@app.route("/review/new", methods=['GET', 'POST'])
@login_required
def new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, rating=form.rating.data, content=form.content.data, writer=current_user)
        db.session.add(book)
        db.session.commit()
        flash('Review added', 'success')
        return redirect(url_for('home'))
    return render_template('newreview.html', title='Add Book', form=form, legend='Add Book')


@app.route("/review/<int:review_id>")
def review(review_id):
    book = Book.query.get_or_404(review_id)
    return render_template('review.html', title=book.title, book=book)

@app.route("/review/<int:review_id>/update", methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    book = Book.query.get(review_id)
    if book.writer != current_user:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.rating = form.rating.data
        book.content = form.content.data
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('review', review_id=review_id))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.rating.data = book.rating
        form.content.data = book.content
    return render_template('newreview.html', title='Update Post', form=form, legend='Update Review')

@app.route("/review/<int:review_id>/delete", methods=['POST'])
@login_required
def delete_review(review_id):
    book = Book.query.get(review_id)
    if book.writer != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Review has been deleted', 'success')
    return redirect(url_for('home'))

@app.route("/profile/<string:username>/delete", methods=['POST'])
@login_required
def delete_acct(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>/")
def user_reviews(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    books = Book.query.filter_by(writer=user).order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user.html', books=books, user=user)

@app.route("/review/<string:title>", methods=['GET', 'POST'])
def book_reviews(title):
    page = request.args.get('page', 1, type=int)
    book = Book.query.filter_by(title=title).order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('samereviews.html', book=book)

# @app.route("/search", methods=['GET', 'POST'])
# def search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         api_key = 'AIzaSyD3EAagT7dIAfMal8iAXF6mgyimS_BD6vI'
#         service = build('books', 'v1', developerKey=api_key)
#         search = form.search.data
#         request = service.volumes().list(source='public', q=search)
#         response = request.execute()
#         print ('Found %d books:' % len(response['items']))
#         for book in response.get('items', []):
#           print ('Title: %s, Authors: %s' % (
#             book['volumeInfo']['title'],
#             book['volumeInfo']['authors'])) 
#     return render_template('search.html', title='Add Book', form=form, legend='Add Book')