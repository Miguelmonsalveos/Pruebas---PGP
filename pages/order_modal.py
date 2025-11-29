from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderModal:
    MODAL = (By.ID, "orderModal")
    INPUT_NOMBRE = (By.ID, "name")
    INPUT_PAIS = (By.ID, "country")
    INPUT_CIUDAD = (By.ID, "city")
    INPUT_TARJETA = (By.ID, "card")
    INPUT_MES = (By.ID, "month")
    INPUT_AÑO = (By.ID, "year")
    BTN_COMPRAR = (By.CSS_SELECTOR, "button[onclick='purchaseOrder()']")
    BTN_CERRAR = (By.CSS_SELECTOR, "#orderModal .close")
    CONFIRMACION_TITULO = (By.CSS_SELECTOR, ".sweet-alert.showSweetAlert h2")
    CONFIRMACION_OK = (By.CSS_SELECTOR, ".confirm.btn.btn-lg.btn-primary")

    def __init__(self, navegador, tiempo_espera=10):
        self.navegador = navegador
        self.espera = WebDriverWait(navegador, tiempo_espera)

    def esperar_modal_visible(self):
        self.espera.until(EC.visibility_of_element_located(self.MODAL))

    def diligenciar_formulario(self, nombre: str = "", tarjeta: str = "", mes: str = "", años: str = "", cvv: str = "", pais: str = "", ciudad: str = ""):
        # Llena solo los valores provistos; útil para escenarios negativos
        if nombre is not None:
            self.navegador.find_element(*self.INPUT_NOMBRE).clear()
            self.navegador.find_element(*self.INPUT_NOMBRE).send_keys(nombre)
        if pais is not None:
            self.navegador.find_element(*self.INPUT_PAIS).clear()
            self.navegador.find_element(*self.INPUT_PAIS).send_keys(pais)
        if ciudad is not None:
            self.navegador.find_element(*self.INPUT_CIUDAD).clear()
            self.navegador.find_element(*self.INPUT_CIUDAD).send_keys(ciudad)
        if tarjeta is not None:
            self.navegador.find_element(*self.INPUT_TARJETA).clear()
            self.navegador.find_element(*self.INPUT_TARJETA).send_keys(tarjeta)
        if mes is not None:
            self.navegador.find_element(*self.INPUT_MES).clear()
            self.navegador.find_element(*self.INPUT_MES).send_keys(mes)
        if años is not None:
            self.navegador.find_element(*self.INPUT_AÑO).clear()
            self.navegador.find_element(*self.INPUT_AÑO).send_keys(años)

    def enviar(self):
        self.espera.until(EC.element_to_be_clickable(self.BTN_COMPRAR)).click()

    def obtener_titulo_confirmacion(self) -> str:
        return self.espera.until(EC.visibility_of_element_located(self.CONFIRMACION_TITULO)).text

    def aceptar_confirmacion(self):
        self.espera.until(EC.element_to_be_clickable(self.CONFIRMACION_OK)).click()
