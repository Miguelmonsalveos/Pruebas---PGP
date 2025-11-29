from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def esperar_alerta(navegador, timeout=5):
    return WebDriverWait(navegador, timeout).until(EC.alert_is_present())


def aceptar_alerta(navegador, timeout=5):
    alerta = esperar_alerta(navegador, timeout)
    texto = alerta.text
    alerta.accept()
    return texto
