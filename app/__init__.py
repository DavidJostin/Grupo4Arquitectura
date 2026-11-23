"""Crea la aplicación Flask (patrón 'application factory')."""

from flask import Flask

from app.config import Config
from app.extensiones import db, login_manager


def create_app(config_extra: dict | None = None) -> Flask:
    """Arma la app. Las pruebas pasan config_extra para usar otra base de datos."""
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_extra:
        app.config.update(config_extra)

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    from app.rutas import bp as calculadora_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(calculadora_bp)

    # Crea las tablas si no existen (sin migraciones, a propósito).
    with app.app_context():
        from app import modelos  # noqa: F401  (registra las tablas)

        db.create_all()

    return app
