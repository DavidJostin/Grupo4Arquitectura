"""PERSONA 3 · Pruebas de extremo a extremo (Playwright).

El robot usa la página como un estudiante: abre, llena, hace clic y verifica.
El fixture `page` lo da pytest-playwright (un navegador limpio por prueba);
`url_base` viene de tests/conftest.py.

Cada prueba usa un usuario distinto para no depender de las demás.
"""

from datetime import date

from playwright.sync_api import Page, expect

CLAVE = "secreta123"


def registrar(page: Page, url_base: str, usuario: str):
    page.goto(f"{url_base}/registro")
    page.fill("#usuario", usuario)
    page.fill("#clave", CLAVE)
    page.fill("#confirmacion", CLAVE)
    page.get_by_role("button", name="Registrarme").click()


def iniciar_sesion(page: Page, url_base: str, usuario: str):
    page.goto(f"{url_base}/login")
    page.fill("#usuario", usuario)
    page.fill("#clave", CLAVE)
    page.get_by_role("button", name="Entrar").click()


def calcular(page: Page):
    page.fill("#viajes", "2")
    page.fill("#dias", "20")
    page.fill("#fecha", "2026-11-18")
    page.get_by_role("button", name="Calcular").click()


def test_estudiante_se_registra(page: Page, url_base: str):
    registrar(page, url_base, "ana")

    # Después de registrarse lo manda al login con un aviso de éxito.
    expect(page).to_have_url(f"{url_base}/login")
    expect(page.locator(".aviso-exito")).to_have_text("Cuenta creada. Ahora inicia sesión.")


def test_estudiante_inicia_sesion(page: Page, url_base: str):
    registrar(page, url_base, "luis")
    iniciar_sesion(page, url_base, "luis")

    # Ya dentro: ve la calculadora y el menú con "Cerrar sesión".
    expect(page.locator("h1")).to_have_text("Calculadora de pasajes")
    expect(page.get_by_role("link", name="Cerrar sesión")).to_be_visible()

    # La fecha viene con la fecha de hoy por defecto.
    expect(page.locator("#fecha")).to_have_value(date.today().isoformat())


def test_estudiante_calcula_su_gasto_mensual(page: Page, url_base: str):
    registrar(page, url_base, "maria")
    iniciar_sesion(page, url_base, "maria")
    calcular(page)

    # Con el ERROR INTENCIONAL 3 esta prueba queda en ROJO.
    expect(page.locator("#total")).to_have_text("$14.00")

    # Detalle: 2 x 20 = 40 pasajes a $0.35.
    expect(page.locator("#detalle")).to_contain_text("40")
    expect(page.locator("#detalle")).to_contain_text("$0.35")
    # Comparación: con la tarifa de 2027 serían $2.00 más.
    expect(page.locator("#comparacion")).to_contain_text("$2.00 más")

    # El formulario conserva lo que escribió.
    expect(page.locator("#viajes")).to_have_value("2")
    expect(page.locator("#dias")).to_have_value("20")


def test_el_calculo_aparece_en_el_historial_y_se_puede_eliminar(page: Page, url_base: str):
    registrar(page, url_base, "pedro")
    iniciar_sesion(page, url_base, "pedro")
    calcular(page)

    page.get_by_role("link", name="Historial").click()

    # Con el ERROR INTENCIONAL 3 esta prueba también queda en ROJO,
    # porque el cálculo nunca se llega a guardar.
    fila = page.locator("#historial tbody tr").first
    expect(fila).to_contain_text("18/11/2026")
    expect(fila).to_contain_text("$14.00")

    # Resumen de arriba: 1 cálculo y $14.00 acumulado.
    expect(page.locator("#numero-calculos")).to_have_text("1")
    expect(page.locator("#total-acumulado")).to_have_text("$14.00")

    # Eliminar: el navegador pregunta "¿Eliminar este cálculo?" y aceptamos.
    page.once("dialog", lambda dialogo: dialogo.accept())
    fila.get_by_role("button", name="Eliminar").click()

    expect(page.locator(".aviso-exito")).to_have_text("Cálculo eliminado.")
    expect(page.locator("#sin-calculos")).to_be_visible()
