"""Extensiones de Flask.

Se crean aquí, sin app, para poder importarlas desde cualquier archivo
sin importaciones circulares. create_app() las conecta con la app.
"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"  # a dónde mandar si no hay sesión
login_manager.login_message = "Inicia sesión para usar la calculadora."
