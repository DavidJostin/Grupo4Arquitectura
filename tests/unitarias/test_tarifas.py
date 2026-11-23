"""PERSONA 1 · Pruebas unitarias de la lógica de negocio (pytest).

Prueban la lógica sin abrir el navegador: son rápidas y van en la base
de la pirámide de pruebas.
"""

from datetime import date
from decimal import Decimal

import pytest

from app.tarifas import formato_dinero, gasto_mensual, tarifa


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
