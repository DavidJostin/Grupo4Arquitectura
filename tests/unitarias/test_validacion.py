"""PERSONA 1 · Pruebas unitarias de la validación de formularios (pytest).

validar_calculo() y validar_registro() devuelven una lista de errores:
lista vacía significa que los datos están bien.
"""

import pytest

from app.validacion import validar_calculo, validar_registro


def test_datos_correctos_no_tienen_errores():
    assert validar_calculo("2", "20", "2026-11-18") == []


@pytest.mark.parametrize("viajes", ["-1", "2.5", "dos", ""])
def test_viajes_deben_ser_enteros_no_negativos(viajes):
    errores = validar_calculo(viajes, "20", "2026-11-18")
    assert errores == ["Los viajes por día deben ser un número entero de 0 en adelante."]


@pytest.mark.parametrize("dias", ["32", "-5"])
def test_dias_deben_estar_entre_0_y_31(dias):
    errores = validar_calculo("2", dias, "2026-11-18")
    assert errores == ["Los días al mes deben ser un número entero entre 0 y 31."]


def test_registro_con_contrasenas_distintas():
    errores = validar_registro("ana", "secreta123", "otra-clave")
    assert errores == ["Las contraseñas no coinciden."]
