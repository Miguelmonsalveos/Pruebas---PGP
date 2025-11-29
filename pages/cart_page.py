from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    LINK_CARRITO = (By.ID, "cartur")
    FILAS_CARRITO = (By.CSS_SELECTOR, "#tbodyid > tr")
    BTN_ELIMINAR = (By.LINK_TEXT, "Delete")
    BTN_PLACE_ORDER = (By.CSS_SELECTOR, "button[data-target='#orderModal']")
    LABEL_TOTAL = (By.ID, "totalp")

    def __init__(self, navegador, tiempo_espera=10):
        self.navegador = navegador
        self.espera = WebDriverWait(navegador, tiempo_espera)

    def abrir_carrito(self):
        self.espera.until(EC.element_to_be_clickable(self.LINK_CARRITO)).click()

    def obtener_filas(self):
        return self.espera.until(EC.presence_of_all_elements_located(self.FILAS_CARRITO))

    def eliminar_primer_item(self):
        filas = self.obtener_filas()
        if not filas:
            raise AssertionError("No items to delete")
        filas[0].find_element(*self.BTN_ELIMINAR).click()

    def click_place_order(self):
        self.espera.until(EC.element_to_be_clickable(self.BTN_PLACE_ORDER)).click()

    def obtener_total(self) -> int:
        texto = self.espera.until(EC.visibility_of_element_located(self.LABEL_TOTAL)).text
        return int(texto) if texto else 0
