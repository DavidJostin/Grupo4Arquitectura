"""Tablas de la base de datos: Usuario y Calculo."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensiones import db, login_manager


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    # Nunca guardamos la contraseña, solo su hash.
    clave_hash = db.Column(db.String(256), nullable=False)

    calculos = db.relationship("Calculo", backref="usuario", lazy=True)

    def poner_clave(self, clave: str) -> None:
        self.clave_hash = generate_password_hash(clave)

    def revisar_clave(self, clave: str) -> bool:
        return check_password_hash(self.clave_hash, clave)


class Calculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    viajes = db.Column(db.Integer, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    # Guardamos el total como texto ("$14.00"): SQLite no tiene tipo decimal
    # y así no perdemos centavos por redondeo.
    total = db.Column(db.String(20), nullable=False)


@login_manager.user_loader
def cargar_usuario(usuario_id: str):
    """Flask-Login llama a esta función para saber quién está en la sesión."""
    return db.session.get(Usuario, int(usuario_id))
