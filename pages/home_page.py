import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class HomePage:
    BTN_CATEGORIA = (By.CSS_SELECTOR, "#contcont .list-group a")
    TARJETA_PRODUCTO = (By.CSS_SELECTOR, ".hrefch")  

    def __init__(self, navegador, tiempo_espera=10):
        self.navegador = navegador
        self.espera = WebDriverWait(navegador, tiempo_espera)

    def abrir(self, url_base: str):
        self.navegador.get(url_base)
        return self

    def seleccionar_categoria(self, nombre_categoria: str):
        botones = self.espera.until(EC.presence_of_all_elements_located(self.BTN_CATEGORIA))
        for boton in botones:
            if boton.text.strip().lower() == nombre_categoria.lower():
                boton.click()
             
                self.espera.until(EC.presence_of_all_elements_located(self.TARJETA_PRODUCTO))
                return
        raise AssertionError(f"Categoria '{nombre_categoria}' no encontrada")

    def abrir_primer_producto(self):

        for _ in range(3):
            try:
                tarjetas = self.espera.until(EC.presence_of_all_elements_located(self.TARJETA_PRODUCTO))
                if not tarjetas:
                    raise AssertionError("No se encontraron productos en la categoría")
                self.espera.until(EC.element_to_be_clickable(self.TARJETA_PRODUCTO))
                self.navegador.execute_script("arguments[0].scrollIntoView(true);", tarjetas[0])
                tarjetas[0].click()
                return
            except StaleElementReferenceException:
                time.sleep(0.5)
        raise AssertionError("No se pudo hacer clic en el primer producto (stale).")
