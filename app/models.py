from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import MetaData, String, Integer, ForeignKey, Text, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

db = SQLAlchemy(model_class=Base)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'))

    def can(self, action):
        ADMIN_ROLE_ID = 1
        MODERATOR_ROLE_ID = 2
        USER_ROLE_ID = 3
        if self.role_id:
            if action == 'add_book':
                return self.role_id == ADMIN_ROLE_ID
            elif action == 'edit_book':
                return self.role_id in [ADMIN_ROLE_ID, MODERATOR_ROLE_ID]
            elif action == 'delete_book':
                return self.role_id == ADMIN_ROLE_ID
        return False

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return True


class BooksGenres(Base):
    __tablename__ = 'books_genres'

    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey('genres.id'), primary_key=True)


class Book(Base):
    __tablename__ = 'books'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    publisher: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    cover_id: Mapped[int] = mapped_column(Integer, ForeignKey('covers.id', ondelete='RESTRICT'))


class Cover(Base):
    __tablename__ = 'covers'

    id = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(255), nullable=False)
    md5_hash: Mapped[str] = mapped_column(String(255), nullable=False)


class Genre(Base):
    __tablename__ = 'genres'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Review(Base):
    __tablename__ = 'reviews'

    id = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=db.func.current_timestamp())

    def prepare_to_html(self):
        self.text = self.text.replace('\n', '<br>')


class Role(Base):
    __tablename__ = 'roles'

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)