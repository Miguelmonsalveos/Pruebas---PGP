import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.waits import aceptar_alerta


@pytest.mark.parametrize(
    "categoria",
    ["Phones", "Laptops", "Monitors"],
)
def test_agregar_productos_carrito(driver, config, categoria):
    """
    Caso 1: Agregar al carrito desde distintas categorías y validar que el ítem aparece y el total > 0.
    """
    home = HomePage(driver, config["explicit_wait"]).abrir(config["base_url"])
    home.seleccionar_categoria(categoria)
    home.abrir_primer_producto()

    product = ProductPage(driver, config["explicit_wait"])
    product.esperar_cargado()
    titulo = product.obtener_titulo()
    product.agregar_al_carrito()
    texto_alerta = aceptar_alerta(driver)
    assert "Product added" in texto_alerta

    cart = CartPage(driver, config["explicit_wait"])
    cart.abrir_carrito()
    filas = cart.obtener_filas()
    assert any(titulo in fila.text for fila in filas), "Producto no aparece en el carrito"
    assert cart.obtener_total() > 0
