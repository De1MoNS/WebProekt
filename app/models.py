from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    # авторизация и права доступа
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # хеширует пароль и сохраняет его
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # проверяет пароль с хешем
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Movie(db.Model):
    # модель фильма
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'description': self.description
        }


class Series(db.Model):
    # модель сериала
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    seasons = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'seasons': self.seasons,
            'genre': self.genre,
            'description': self.description
        }


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
