import os
import csv
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml


def cargar_config():
    ruta_cfg = Path("config/config.yaml")
    with ruta_cfg.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cargar_datos_ordenes():
    archivo = Path("data/orders.csv")
    filas = []
    with archivo.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            fila["espera_exito"] = fila["espera_exito"].lower() == "true"
            filas.append(fila)
    return filas


@pytest.fixture(scope="session")
def config():
    return cargar_config()


@pytest.fixture
def driver(config):
    navegador_cfg = os.environ.get("BROWSER", config.get("browser", "chrome")).lower()
    modo_headless = config.get("headless", False)

    if navegador_cfg == "chrome":
        opciones = ChromeOptions()
        if modo_headless:
            opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=opciones)
    elif navegador_cfg == "firefox":
        opciones = FirefoxOptions()
        if modo_headless:
            opciones.add_argument("--headless")
        opciones.add_argument("--width=1920")
        opciones.add_argument("--height=1080")
        driver = webdriver.Firefox(options=opciones)
    else:
        raise RuntimeError(f"Navegador no soportado: {navegador_cfg}")

    driver.implicitly_wait(config.get("implicit_wait", 5))
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def datos_ordenes():
    return cargar_datos_ordenes()


def pytest_terminal_summary(terminalreporter, exitstatus, config):  # pylint: disable=unused-argument
    """
    Genera un resumen en texto plano con totales, porcentajes y detalle de casos en reports/resumen.txt.
    """
    total = terminalreporter._numcollected  # type: ignore[attr-defined]
    fallidos = len(terminalreporter.stats.get("failed", []))
    pasados = len(terminalreporter.stats.get("passed", []))
    omitidos = len(terminalreporter.stats.get("skipped", []))
    errores = len(terminalreporter.stats.get("error", []))

    if total == 0:
        return

    pct_ok = round((pasados / total) * 100, 2)
    pct_fail = round((fallidos / total) * 100, 2)

    # Mapea cada archivo a un nombre más legible de caso
    alias_casos = {
        "tests/test_agregar_carrito.py": "Caso 1 - Agregar al carrito",
        "tests/test_gestion_carrito.py": "Caso 2 - Gestionar carrito",
        "tests/test_place_order_datos.py": "Caso 3 - Place Order (válidos e inválidos)",
    }

    detalles = []
    for estado in ("passed", "failed", "error", "skipped"):
        for rep in terminalreporter.stats.get(estado, []):
            nodo = rep.nodeid  # ejemplo: tests/test_agregar_carrito.py::test_agregar_productos_carrito[Phones]
            archivo = nodo.split("::")[0]
            alias = alias_casos.get(archivo, archivo)
            detalles.append(f"{alias} | {nodo} | estado: {estado.upper()}")

    resumen = [
        "Resumen de ejecución de pruebas",
        f"Total pruebas: {total}",
        f"Pasadas: {pasados}",
        f"Fallidas: {fallidos}",
        f"Omitidas: {omitidos}",
        f"Errores: {errores}",
        f"Porcentaje OK: {pct_ok}%",
        f"Porcentaje Fallo: {pct_fail}%",
        "",
        "Detalle por caso:",
        *detalles,
    ]

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    resumen_path = reports_dir / "resumen.txt"
    resumen_path.write_text("\n".join(resumen), encoding="utf-8")

    # También imprime el path en consola para referencia
    terminalreporter.write_sep("-", f"Resumen escrito en {resumen_path}")
