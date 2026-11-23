"""Lógica de negocio: tarifa del pasaje urbano de Quito y gasto mensual.

Dato real: el Concejo Metropolitano aprobó el 8 de septiembre de 2026 que el
pasaje urbano pase de $0.35 a $0.40 desde el 1 de enero de 2027.

Usamos Decimal (y no float) porque es dinero: con float, 0.1 + 0.2 no da 0.3.
"""

from datetime import date
from decimal import Decimal

TARIFA_ACTUAL = Decimal("0.35")
TARIFA_NUEVA = Decimal("0.40")
FECHA_CAMBIO = date(2027, 1, 1)


def tarifa(fecha: date) -> Decimal:
    """Devuelve el precio de un pasaje en la fecha indicada.

    ERROR INTENCIONAL 2 (lo detecta pytest):
    usa > en lugar de >=, así que el 1 de enero de 2027 todavía cobra $0.35.
    Corrección: if fecha >= FECHA_CAMBIO:
    """
    if fecha > FECHA_CAMBIO:
        return TARIFA_NUEVA
    return TARIFA_ACTUAL


def gasto_mensual(viajes_por_dia: int, dias: int, fecha: date) -> Decimal:
    """Gasto del mes: viajes por día x días x tarifa."""
    if viajes_por_dia < 0 or dias < 0:
        raise ValueError("Los viajes y los días no pueden ser negativos")
    return viajes_por_dia * dias * tarifa(fecha)


def formato_dinero(valor: Decimal) -> str:
    """Convierte 14 en '$14.00'."""
    return f"${valor:.2f}"
