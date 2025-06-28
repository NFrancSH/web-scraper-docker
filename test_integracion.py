from WebScraping import analizar_seguridad
from selenium import webdriver
import pytest

@pytest.fixture
def setup_chrome_driver():
    driver = webdriver.Chrome()  # Necesitas chromedriver instalado
    yield driver
    driver.quit()

def test_integracion_selenium_ssl():
    resultado = analizar_seguridad("https://example.com")
    
    assert isinstance(resultado, dict)
    assert resultado["ssl"] is True
    assert resultado["certificado"] is not None  # ¡Ahora pasa!
    
    if resultado.get("error"):
        pytest.fail(f"Error en análisis: {resultado['error']}")