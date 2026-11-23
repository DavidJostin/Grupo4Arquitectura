"""Validación de formularios.

Funciones de Python puro (sin Flask): reciben el texto que escribió el
usuario y devuelven una lista de mensajes de error. Lista vacía = todo bien.
Así se pueden probar con pytest sin abrir el navegador.
"""

from datetime import date

DIAS_MAXIMOS = 31


def es_entero_no_negativo(texto: str) -> bool:
    """'20' -> True; '-1', '2.5', 'dos' o '' -> False."""
    return texto.strip().isdigit()


def validar_calculo(viajes: str, dias: str, fecha: str) -> list[str]:
    errores = []

    if not es_entero_no_negativo(viajes):
        errores.append("Los viajes por día deben ser un número entero de 0 en adelante.")

    if not es_entero_no_negativo(dias) or int(dias) > DIAS_MAXIMOS:
        errores.append(f"Los días al mes deben ser un número entero entre 0 y {DIAS_MAXIMOS}.")

    try:
        date.fromisoformat(fecha)
    except ValueError:
        errores.append("Ingresa una fecha válida.")

    return errores


def validar_registro(nombre: str, clave: str, confirmacion: str) -> list[str]:
    errores = []

    if not 3 <= len(nombre.strip()) <= 20:
        errores.append("El usuario debe tener entre 3 y 20 caracteres.")

    if len(clave) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")

    if clave != confirmacion:
        errores.append("Las contraseñas no coinciden.")

    return errores
