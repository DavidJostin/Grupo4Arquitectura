"""Rutas de la calculadora: formulario, cálculo e historial."""

from datetime import date
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensiones import db
from app.modelos import Calculo
from app.tarifas import (
    comparar_tarifas,
    formato_dinero,
    gasto_mensual,
    leer_dinero,
    pasajes_del_mes,
    tarifa,
)
from app.validacion import validar_calculo

bp = Blueprint("calculadora", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def inicio():
    total = None
    detalle = None
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

            # Datos extra para mostrar el detalle y la comparación 2026 vs 2027.
            comparacion = comparar_tarifas(viajes, dias)
            detalle = {
                "pasajes": pasajes_del_mes(viajes, dias),
                "tarifa": formato_dinero(tarifa(fecha)),
                "con_2026": formato_dinero(comparacion["con_2026"]),
                "con_2027": formato_dinero(comparacion["con_2027"]),
                "diferencia": formato_dinero(comparacion["diferencia"]),
            }

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
            flash("Cálculo guardado en tu historial.", "exito")

    return render_template(
        "index.html",
        total=total,
        detalle=detalle,
        errores=errores,
        hoy=date.today().isoformat(),  # fecha por defecto del formulario
    )


@bp.route("/historial")
@login_required
def historial():
    calculos = (
        Calculo.query.filter_by(usuario_id=current_user.id)
        .order_by(Calculo.id.desc())
        .all()
    )
    # Resumen: suma de todos los totales guardados ("$14.00" -> 14.00).
    acumulado = sum((leer_dinero(c.total) for c in calculos), Decimal("0"))
    return render_template(
        "historial.html", calculos=calculos, acumulado=formato_dinero(acumulado)
    )


@bp.route("/historial/<int:calculo_id>/eliminar", methods=["POST"])
@login_required
def eliminar(calculo_id):
    # Filtramos también por usuario: nadie puede borrar cálculos ajenos.
    calculo = Calculo.query.filter_by(
        id=calculo_id, usuario_id=current_user.id
    ).first_or_404()
    db.session.delete(calculo)
    db.session.commit()
    flash("Cálculo eliminado.", "exito")
    return redirect(url_for("calculadora.historial"))
