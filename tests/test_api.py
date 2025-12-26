import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    # создание тестового клиента
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            u = User(username='test', email='test@test.com')
            u.set_password('pass')
            db.session.add(u)
            db.session.commit()
        yield client


def test_get_movies(client):
    rv = client.get('/api/movies')
    assert rv.status_code == 200
    assert isinstance(rv.json, list)
