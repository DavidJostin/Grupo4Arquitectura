"""Rutas de cuentas: registrarse, iniciar sesión y cerrar sesión."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensiones import db
from app.modelos import Usuario
from app.validacion import validar_registro

bp = Blueprint("auth", __name__)


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    errores = []

    if request.method == "POST":
        nombre = request.form["usuario"].strip()
        clave = request.form["clave"]
        confirmacion = request.form["confirmacion"]

        errores = validar_registro(nombre, clave, confirmacion)
        if not errores and Usuario.query.filter_by(nombre=nombre).first():
            errores.append("Ese usuario ya existe. Elige otro.")

        if not errores:
            usuario = Usuario(nombre=nombre)
            usuario.poner_clave(clave)
            db.session.add(usuario)
            db.session.commit()
            flash("Cuenta creada. Ahora inicia sesión.", "exito")
            return redirect(url_for("auth.login"))

    return render_template("registro.html", errores=errores)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("calculadora.inicio"))

    errores = []

    if request.method == "POST":
        nombre = request.form["usuario"].strip()
        clave = request.form["clave"]
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and usuario.revisar_clave(clave):
            login_user(usuario)
            return redirect(url_for("calculadora.inicio"))

        # Mensaje genérico: no decimos si falló el usuario o la contraseña.
        errores.append("Usuario o contraseña incorrectos.")

    return render_template("login.html", errores=errores)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Cerraste sesión.", "info")
    return redirect(url_for("auth.login"))
