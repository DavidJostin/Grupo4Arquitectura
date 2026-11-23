"""PERSONA 1 · Pruebas unitarias de la lógica de negocio (pytest).

Prueban la lógica sin abrir el navegador: son rápidas y van en la base
de la pirámide de pruebas.
"""

from datetime import date
from decimal import Decimal

import pytest

from app.tarifas import (
    comparar_tarifas,
    formato_dinero,
    gasto_mensual,
    leer_dinero,
    pasajes_del_mes,
    tarifa,
)


def test_tarifa_en_2026_es_35_centavos():
    assert tarifa(date(2026, 11, 18)) == Decimal("0.35")


def test_tarifa_desde_el_1_de_enero_de_2027_es_40_centavos():
    # Con el ERROR INTENCIONAL 2 esta prueba queda en ROJO.
    assert tarifa(date(2027, 1, 1)) == Decimal("0.40")


def test_gasto_mensual_de_un_estudiante():
    # 2 viajes x 20 días x $0.35 = $14.00
    assert gasto_mensual(2, 20, date(2026, 11, 18)) == Decimal("14.00")


def test_formato_dinero_muestra_dos_decimales():
    assert formato_dinero(Decimal("14")) == "$14.00"


def test_no_acepta_valores_negativos():
    with pytest.raises(ValueError):
        gasto_mensual(-1, 20, date(2026, 11, 18))


def test_pasajes_del_mes():
    # 2 viajes x 20 días = 40 pasajes
    assert pasajes_del_mes(2, 20) == 40


def test_comparar_tarifas_2026_contra_2027():
    # 40 pasajes: $14.00 con $0.35 y $16.00 con $0.40 -> $2.00 más
    comparacion = comparar_tarifas(2, 20)
    assert comparacion["con_2026"] == Decimal("14.00")
    assert comparacion["con_2027"] == Decimal("16.00")
    assert comparacion["diferencia"] == Decimal("2.00")


def test_leer_dinero_es_lo_contrario_de_formato_dinero():
    assert leer_dinero("$14.00") == Decimal("14.00")
    assert leer_dinero(formato_dinero(Decimal("2.5"))) == Decimal("2.50")
