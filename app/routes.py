from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from flask_login import login_required, current_user
from auth import check_perm
from werkzeug.utils import secure_filename
from models import db, BooksGenres, Book, Review, Genre, Cover, User
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
import os
import hashlib
import bleach
import config

bp = Blueprint('routes', __name__, url_prefix='/routes')

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)
    offset = (page - 1) * per_page

    # Subquery for reviews
    review_subquery = db.session.query(
        Book.id.label('book_id'),
        func.avg(Review.rating).label('average_rating'),
        func.count(Review.id).label('review_count')
    ).outerjoin(
        Review, Book.id == Review.book_id
    ).group_by(Book.id).subquery(name='review_subquery')

    # Subquery for genres
    genre_subquery = db.session.query(
        BooksGenres.book_id,
        func.group_concat(Genre.name.op('SEPARATOR')(', ')).label('genres')
    ).join(
        Genre, BooksGenres.genre_id == Genre.id
    ).group_by(BooksGenres.book_id).subquery(name='genre_subquery')

    # Main query
    query = db.session.query(
        Book.id,
        Book.title,
        Book.year,
        genre_subquery.c.genres,
        Cover.filename,
        review_subquery.c.average_rating,
        review_subquery.c.review_count
    ).outerjoin(
        genre_subquery, Book.id == genre_subquery.c.book_id
    ).join(
        Cover, Book.cover_id == Cover.id
    ).outerjoin(
        review_subquery, Book.id == review_subquery.c.book_id
    ).order_by(Book.year.desc()).offset(offset).limit(per_page)

    books = query.all()
    total_books = db.session.query(func.count(Book.id)).scalar()

    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total_books,
        'pages': total_books // per_page + (1 if total_books % per_page > 0 else 0),
        'has_prev': page > 1,
        'has_next': page * per_page < total_books,
        'next_num': page + 1,
        'prev_num': page - 1,
    }

    return render_template('index.html', current_user=current_user, books=books, pagination=pagination)

@bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    genres = db.session.query(Genre).join(BooksGenres).filter(BooksGenres.book_id == book_id).all()
    cover = db.session.query(Cover).get(book.cover_id)

    reviews = db.session.query(
        Review.rating.label('review_rating'),
        Review.text.label('review_text'),
        Review.date_added.label('date_added'),
        User.first_name.label('author_first_name')
    ).join(
        User, User.id == Review.user_id
    ).filter(
        Review.book_id == book_id
    ).order_by(
        Review.date_added.desc()
    ).all()

    # Calculate the average rating and review count
    average_rating = db.session.query(func.avg(Review.rating)).filter(Review.book_id == book_id).scalar()
    review_count = db.session.query(func.count(Review.id)).filter(Review.book_id == book_id).scalar()

    # Fetch the current user's review if authenticated
    user_review = None
    if current_user.is_authenticated:
        user_review = db.session.query(Review).filter(Review.book_id == book_id, Review.user_id == current_user.id).first()

    return render_template(
        'books/book_detail.html',
        book=book,
        genres=genres,
        cover=cover,
        reviews=reviews,
        average_rating=average_rating,
        review_count=review_count,
        user_review=user_review
    )

@bp.route('/review/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_review(book_id):
    if request.method == 'POST':
        rating = request.form.get('rating')
        text = bleach.clean(request.form.get('text'))

        if not rating or not text:
            flash('Все поля должны быть заполнены.', 'error')
            return redirect(url_for('routes.add_review', book_id=book_id))

        try:
            rating = int(rating)
            if rating < 0 or rating > 5:
                flash('Рейтинг должен быть между 0 и 5.', 'error')
                return redirect(url_for('routes.add_review', book_id=book_id))

            review = Review(
                book_id=book_id,
                user_id=current_user.id,
                rating=rating,
                text=bleach.clean(text)
            )
            db.session.add(review)
            db.session.commit()
            flash('Отзыв добавлен.', 'success')
            return redirect(url_for('routes.book_detail', book_id=book_id))
        except ValueError:
            flash('Рейтинг должен быть числом.', 'error')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Ошибка базы данных: {str(e)}', 'error')

    return render_template('books/reviews_form.html', book_id=book_id)

@bp.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@check_perm("edit_book")
def edit_book(book_id):
    book = db.session.query(Book).get_or_404(book_id)
    genres = db.session.query(Genre).all()

    if request.method == 'POST':
        try:
            book.title = request.form['title']
            book.description = bleach.clean(request.form['description'])
            book.year = int(request.form['year'])
            book.publisher = request.form['publisher']
            book.author = request.form['author']
            book.pages = int(request.form['pages'])
            genre_ids = request.form.getlist('genres')

            db.session.query(BooksGenres).filter_by(book_id=book.id).delete()

            for genre_id in genre_ids:
                book_genre = BooksGenres(book_id=book.id, genre_id=genre_id)
                db.session.add(book_genre)

            db.session.commit()
            flash('Книга успешно обновлена', 'success')
            return redirect(url_for('routes.book_detail', book_id=book.id))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Ошибка базы данных: {str(e)}', 'error')

        except ValueError as e:
            flash(f'Некорректное значение: {str(e)}', 'error')

        except Exception as e:
            flash(f'Неизвестная ошибка: {str(e)}', 'error')

    return render_template('books/edit_book.html', book=book, genres=genres)

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
        description = bleach.clean(request.form.get('description'))
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
                book_genre = BooksGenres(book_id=book.id, genre_id=genre_id)
                db.session.add(book_genre)

            db.session.commit()

            flash('Книга успешно добавлена.')
            return redirect(url_for('routes.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'При сохранении данных возникла ошибка: {str(e)}. Проверьте корректность введённых данных.', 'error')
            return render_template('add_book.html', genres=db.session.query(Genre).all())

    return render_template('books/add_book.html', genres=db.session.query(Genre).all())