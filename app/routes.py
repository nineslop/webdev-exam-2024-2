from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import app
from .extensions import db
from .models import Book, Review, Genre, Cover
from .auth import role_required
from .forms import ReviewForm
from werkzeug.utils import secure_filename
import os
import hashlib

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.year.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', current_user=current_user, books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/review/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_review(book_id):
    if request.method == 'POST':
        review = Review(
            book_id=book_id,
            user_id=current_user.id,
            rating=request.form['rating'],
            text=request.form['text']
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('book_detail', book_id=book_id))
    return render_template('review_form.html', book_id=book_id)

@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'moderator')
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        try:
            book.title = request.form['title']
            book.description = bleach.clean(request.form['description'])
            book.year = request.form['year']
            book.publisher = request.form['publisher']
            book.author = request.form['author']
            book.pages = request.form['pages']
            book.genres = Genre.query.filter(Genre.id.in_(request.form.getlist('genres'))).all()
            db.session.commit()
            return redirect(url_for('book_detail', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'error')
            return render_template('edit_book.html', book=book, genres=Genre.query.all())
    return render_template('edit_book.html', book=book, genres=Genre.query.all())

@app.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        Review.query.filter_by(book_id=book.id).delete()
        if book.cover:
            cover = Cover.query.get(book.cover_id)
            if cover:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], cover.filename))
                    db.session.delete(cover)
                except:
                    pass
        db.session.delete(book)
        db.session.commit()
        flash('Книга успешно удалена.')
    except Exception as e:
        db.session.rollback()
        flash('При удалении книги возникла ошибка.', 'error')
    return redirect(url_for('index'))

@app.route('/book/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_book():
    if request.method == 'POST':
        try:
            file = request.files['cover']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            cover = Cover.query.filter_by(md5_hash=file_hash).first()
            if not cover:
                cover = Cover(filename=filename, mime_type=file.mimetype, md5_hash=file_hash)
                db.session.add(cover)
                db.session.flush()

            book = Book(
                title=request.form['title'],
                description=bleach.clean(request.form['description']),
                year=request.form['year'],
                publisher=request.form['publisher'],
                author=request.form['author'],
                pages=request.form['pages'],
                cover_id=cover.id
            )
            db.session.add(book)
            db.session.commit()
            flash('Книга успешно добавлена.')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'error')
            return render_template('add_book.html', genres=Genre.query.all())
    return render_template('add_book.html', genres=Genre.query.all())

@app.route('/book/<int:book_id>/review', methods=['GET', 'POST'])
@login_required
def create_review(book_id):
    form = ReviewForm()
    if form.validate_on_submit():
        rating = form.rating.data
        text = form.text.data
        review = Review(book_id=book_id, user_id=current_user.id, rating=rating, text=text)
        db.session.add(review)
        db.session.commit()
        flash('Ваша рецензия была успешно сохранена', 'success')
        return redirect(url_for('view_book', book_id=book_id))
    
    return render_template('create_review.html', form=form)