from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import MovieForm, SeriesForm
from app.models import Movie, Series
from app import db


@bp.route('/')
def index():
    # главная страница
    movies = Movie.query.all()
    series = Series.query.all()
    return render_template('index.html', movies=movies, series=series)


# фильмы
@bp.route('/movies')
def movies():
    # список фильмов
    items = Movie.query.all()
    return render_template('movies/list.html', items=items)


@bp.route('/movies/new', methods=['GET', 'POST'])
@login_required
def movie_create():
    # форма добавления фильмов
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            year=form.year.data,
            genre=form.genre.data,
            description=form.description.data
        )
        db.session.add(movie)
        db.session.commit()
        flash('Фильм добавлен!')
        return redirect(url_for('main.movies'))
    return render_template('movies/create.html', form=form)


@bp.route('/movies/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def movie_edit(id):
    # форма редактирования фильма
    movie = Movie.query.get_or_404(id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        form.populate_obj(movie)
        db.session.commit()
        flash('Фильм обновлён!')
        return redirect(url_for('main.movies'))
    return render_template('movies/edit.html', form=form)


@bp.route('/movies/<int:id>/delete', methods=['POST'])
@login_required
def movie_delete(id):
    # удаление фильма только для админа
    movie = Movie.query.get_or_404(id)
    if not current_user.is_admin:
        flash('Только администратор может удалять!')
        return redirect(url_for('main.movies'))
    db.session.delete(movie)
    db.session.commit()
    flash('Фильм удалён.')
    return redirect(url_for('main.movies'))


# сериалы
@bp.route('/series')
def series():
    items = Series.query.all()
    return render_template('movies/list.html', items=items, is_series=True)


@bp.route('/series/new', methods=['GET', 'POST'])
@login_required
def series_create():
    form = SeriesForm()
    if form.validate_on_submit():
        s = Series(
            title=form.title.data,
            year=form.year.data,
            seasons=form.seasons.data,
            genre=form.genre.data,
            description=form.description.data
        )
        db.session.add(s)
        db.session.commit()
        flash('Сериал добавлен!')
        return redirect(url_for('main.series'))
    return render_template('movies/create.html', form=form, is_series=True)


@bp.route('/series/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def series_edit(id):
    s = Series.query.get_or_404(id)
    form = SeriesForm(obj=s)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.commit()
        flash('Сериал обновлён!')
        return redirect(url_for('main.series'))
    return render_template('movies/edit.html', form=form, is_series=True)


@bp.route('/series/<int:id>/delete', methods=['POST'])
@login_required
def series_delete(id):
    s = Series.query.get_or_404(id)
    if not current_user.is_admin:
        flash('Только администратор может удалять!')
        return redirect(url_for('main.series'))
    db.session.delete(s)
    db.session.commit()
    flash('Сериал удалён.')
    return redirect(url_for('main.series'))
