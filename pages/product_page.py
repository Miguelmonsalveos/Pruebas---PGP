from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    BTN_AGREGAR_CARRITO = (By.CSS_SELECTOR, "a.btn.btn-success.btn-lg")
    TITULO_PRODUCTO = (By.CSS_SELECTOR, ".name")
    PRECIO_PRODUCTO = (By.CSS_SELECTOR, ".price-container")

    def __init__(self, navegador, tiempo_espera=10):
        self.navegador = navegador
        self.espera = WebDriverWait(navegador, tiempo_espera)

    def esperar_cargado(self):
        self.espera.until(EC.visibility_of_element_located(self.TITULO_PRODUCTO))

    def agregar_al_carrito(self):
        self.espera.until(EC.visibility_of_element_located(self.BTN_AGREGAR_CARRITO))
        self.espera.until(EC.element_to_be_clickable(self.BTN_AGREGAR_CARRITO)).click()

    def obtener_titulo(self) -> str:
        return self.espera.until(EC.visibility_of_element_located(self.TITULO_PRODUCTO)).text

    def obtener_precio_texto(self) -> str:
        return self.espera.until(EC.visibility_of_element_located(self.PRECIO_PRODUCTO)).text
