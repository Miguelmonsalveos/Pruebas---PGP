import time
import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.waits import aceptar_alerta


def test_eliminar_actualiza_total(driver, config):
    """
    Caso 2: Gestionar carrito. Agregar dos productos, eliminar uno y validar total actualizado.
    """
    def agregar_primer_producto_de(categoria):
        home.seleccionar_categoria(categoria)
        home.abrir_primer_producto()
        product = ProductPage(driver, config["explicit_wait"])
        product.esperar_cargado()
        product.agregar_al_carrito()
        aceptar_alerta(driver)
        driver.get(config["base_url"])

    home = HomePage(driver, config["explicit_wait"]).abrir(config["base_url"])
    agregar_primer_producto_de("Phones")
    agregar_primer_producto_de("Laptops")

    cart = CartPage(driver, config["explicit_wait"])
    cart.abrir_carrito()
    filas = cart.obtener_filas()
   
    if len(filas) < 2:
        driver.get(config["base_url"])
        agregar_primer_producto_de("Monitors")
        cart.abrir_carrito()
        filas = cart.obtener_filas()
    assert len(filas) >= 2, "Se esperaban al menos 2 productos"
    total_inicial = cart.obtener_total()

    cart.eliminar_primer_item()
    time.sleep(2)  
    total_final = cart.obtener_total()
    assert total_final < total_inicial, "El total no se actualizó tras eliminar"


def test_persistencia_simple_carrito(driver, config):
    """
    Caso 2 (alterno): Validar que los ítems siguen tras refrescar la página durante la sesión.
    """
    home = HomePage(driver, config["explicit_wait"]).abrir(config["base_url"])
    home.seleccionar_categoria("Phones")
    home.abrir_primer_producto()
    prod = ProductPage(driver, config["explicit_wait"])
    prod.esperar_cargado()
    prod.agregar_al_carrito()
    aceptar_alerta(driver)
    driver.get(config["base_url"])

    cart = CartPage(driver, config["explicit_wait"])
    cart.abrir_carrito()
    filas_antes = cart.obtener_filas()
    assert filas_antes, "No hay ítems en el carrito antes del refresh"
    total_antes = cart.obtener_total()

    driver.refresh()
    filas_despues = cart.obtener_filas()
    total_despues = cart.obtener_total()
    assert len(filas_despues) == len(filas_antes), "Los ítems cambiaron tras refrescar"
    assert total_despues == total_antes, "El total cambió tras refrescar"
