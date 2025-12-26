from flask import Blueprint

# создает blueprint с именем auth
bp = Blueprint('auth', __name__)

from app.auth import routes
