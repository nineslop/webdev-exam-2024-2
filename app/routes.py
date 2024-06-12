from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from flask_login import login_required, current_user
from auth import check_perm
from werkzeug.utils import secure_filename
from models import db, BooksGenres, Book, Review, Genre, Cover
from sqlalchemy import func
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.exc import IntegrityError
import os
import hashlib
import bleach
import config

bp = Blueprint('routes', __name__, url_prefix='/routes')


@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    subquery = db.session.query(
        Book.id,
        func.avg(Review.rating).label('average_rating'),
        func.count(Review.id).label('review_count')
    ).outerjoin(
        Review, Book.id == Review.book_id
    ).group_by(Book.id
    ).subquery()

    query = db.session.query(
        Book.id,
        Book.title,
        Book.year,
        Genre.name,
        Cover.filename
    ).join(
        BooksGenres, Book.id == BooksGenres.book_id
    ).join(
        Genre, BooksGenres.genre_id == Genre.id
    ).join(
        Cover, Book.cover_id == Cover.id
    ).outerjoin(
        subquery, Book.id == subquery.c.id
    ).group_by(Book.id, Book.title, Book.year, Cover.filename, Genre.name
    ).order_by(Book.year.desc())

    page_number = 1
    books_per_page = 10
    books = query.paginate(page=page_number, per_page=books_per_page)

    return render_template('index.html', current_user=current_user, books=books)


@bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    genres = db.session.query(Genre).join(BooksGenres).filter(BooksGenres.book_id == book_id).all()
    cover = db.session.query(Cover).get(book.cover_id)
    return render_template('books/book_detail.html', book=book, genres=genres, cover=cover)


@bp.route('/review/<int:book_id>', methods=['GET', 'POST'])
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

@bp.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@check_perm("edit_book")
def edit_book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    if request.method == 'POST':
        try:
            book.title = request.form['title']
            book.description = bleach.clean(request.form['description'])
            book.year = request.form['year']
            book.publisher = request.form['publisher']
            book.author = request.form['author']
            book.pages = request.form['pages']
            book.genres = db.session.query(Genre).filter(Genre.id.in_(request.form.getlist('genres'))).all()
            db.session.commit()
            return redirect(url_for('book_detail', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'error')
            return render_template('edit_book.html', book=book, genres=db.session.query(Genre).all())
    return render_template('books/edit_book.html', book=book, genres=db.session.query(Genre).all())


@bp.route('/book/delete/<int:book_id>', methods=['GET'])
@login_required
@check_perm('delete_book')
def delete_book(book_id):
    try:
        try:
            book = db.session.query(Book).filter(Book.id == book_id).one()
        except Exception:
            flash("Запрошенная книга не существует", "danger")
            return redirect(url_for("routes.index"))

        db.session.delete(book)
        db.session.commit()
 
        cover = db.session.query(Cover).filter(Cover.id == book.cover_id).one()
        try:
            db.session.delete(cover)
            db.session.commit()
            try:
                os.remove(os.path.join(config.UPLOAD_FOLDER, cover.filename))
            except Exception as e:
                flash(
                    f"Возникла ошибка при удалении обложки книги «{book.title}». ({e})",
                    "danger",
                )
                db.session.rollback()

                return redirect(url_for("routes.index"))
        except Exception:
            pass

        flash(f"Книга «{book.title}» была успешно удалена!", "success")
        return redirect(url_for("routes.index"))
    except Exception as e:
        flash(f"Возникла ошибка при удалении книги «{e}»", "danger")
        db.session.rollback()

        return redirect(url_for("routes.index"))



UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')

@bp.route('/add_book', methods=['GET', 'POST'])
@login_required
@check_perm('add_book')
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        pages = request.form.get('pages')
        description = request.form.get('description')
        genre_ids = request.form.getlist('genres')

        try:
            file = request.files['cover']
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            cover = db.session.query(Cover).filter_by(md5_hash=file_hash).first()
            if not cover:
                cover = Cover(filename=filename, mime_type=file.mimetype, md5_hash=file_hash)
                db.session.add(cover)
                db.session.flush()

            book = Book(
                title=title,
                description=bleach.clean(description),
                year=year,
                publisher=publisher,
                author=author,
                pages=pages,
                cover_id=cover.id
            )
            db.session.add(book)
            db.session.flush()

            if not genre_ids:
                flash('Не выбран ни один жанр.', 'error')
                return render_template('add_book.html', genres=db.session.query(Genre).all())

            for genre_id in genre_ids:
                print(f'Adding genre {genre_id} to book {book.id}')
                book_genre = BooksGenres(book_id=book.id, genre_id=genre_id)
                db.session.add(book_genre)

            db.session.commit()

            flash('Книга успешно добавлена.')
            return redirect(url_for('routes.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'При сохранении данных возникла ошибка: {str(e)}. Проверьте корректность введённых данных.', 'error')
            return render_template('add_book.html', genres=db.session.query(Genre).all())

    return render_template('add_book.html', genres=db.session.query(Genre).all())