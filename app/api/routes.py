from flask import jsonify, request
from flask_login import login_required, current_user
from flasgger import swag_from
from app.api import bp
from app.models import Movie, Series, db


@bp.route('/movies', methods=['GET'])
@swag_from({
    'tags': ['Movies'],
    'responses': {200: {'description': 'Список фильмов'}}
})
def get_movies():
    # получение списка фильмов
    movies = Movie.query.all()
    return jsonify([m.to_dict() for m in movies])


@bp.route('/movies', methods=['POST'])
@login_required
@swag_from({'tags': ['Movies'], 'responses': {201: {'description': 'Фильм создан'}}})
def create_movie():
    # создание фильма
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        year=data.get('year'),
        genre=data.get('genre'),
        description=data.get('description')
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict()), 201


@bp.route('/movies/<int:id>', methods=['DELETE'])
@login_required
@swag_from({'tags': ['Movies'], 'responses': {200: {'description': 'Фильм удалён'}}})
def delete_movie(id):
    # удаление фильма
    if not current_user.is_admin:
        return jsonify({'error': 'Только администратор'}), 403
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Удалено'})
