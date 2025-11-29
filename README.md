# Pruebas DemoBlaze (Selenium + pytest)

Estructura base para 3 casos automatizados:
1) Agregar al carrito (RF-DB-001).
2) Gestionar carrito: agregar/eliminar y persistencia en sesión.
3) Place Order con datos válidos e inválidos (RF-DB-002).

## Estructura
- `config/config.yaml`: URL, navegador y tiempos de espera.
- `data/orders.csv`: datos de entrada para Place Order (válidos/inválidos).
- `pages/`: Page Objects (home, producto, carrito, modal de orden).
- `tests/`: suites de pytest separadas por caso.
- `utils/`: ayudas para waits/alertas.

## Cómo ejecutar (local)
1) Crear venv e instalar dependencias: `pip install -r requirements.txt` (Selenium, pytest, pyyaml).
2) Ajustar `config/config.yaml` si es necesario (navegador/headless).
3) Ejecutar pruebas: `pytest -v`.


## Notas
- Datos para Place Order vienen de `data/orders.csv`. Puedes agregar más filas sin tocar el código.
- El navegador se puede forzar con env var: `BROWSER=firefox pytest -v`.
- Las pruebas asumen DemoBlaze pública: https://www.demoblaze.com
