"""Rutas de la calculadora: formulario, cálculo e historial."""

from datetime import date

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.extensiones import db
from app.modelos import Calculo
from app.tarifas import formato_dinero, gasto_mensual
from app.validacion import validar_calculo

bp = Blueprint("calculadora", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def inicio():
    total = None
    errores = []

    if request.method == "POST":
        errores = validar_calculo(
            request.form["viajes"], request.form["dias"], request.form["fecha"]
        )

        if not errores:
            # ERROR INTENCIONAL 3 (lo detecta Playwright):
            # los datos del formulario llegan como texto ("2", "20") y no se
            # convierten a número. Al usarlos en el cálculo, Python falla y la
            # página responde con un error 500.
            # Corrección:
            #     viajes = int(request.form["viajes"])
            #     dias = int(request.form["dias"])
            viajes = request.form["viajes"]
            dias = request.form["dias"]
            fecha = date.fromisoformat(request.form["fecha"])

            total = formato_dinero(gasto_mensual(viajes, dias, fecha))

            # Guardamos el cálculo en el historial del usuario.
            calculo = Calculo(
                usuario_id=current_user.id,
                fecha=fecha,
                viajes=viajes,
                dias=dias,
                total=total,
            )
            db.session.add(calculo)
            db.session.commit()

    return render_template("index.html", total=total, errores=errores)


@bp.route("/historial")
@login_required
def historial():
    calculos = (
        Calculo.query.filter_by(usuario_id=current_user.id)
        .order_by(Calculo.id.desc())
        .all()
    )
    return render_template("historial.html", calculos=calculos)
