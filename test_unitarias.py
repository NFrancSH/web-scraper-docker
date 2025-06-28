import pytest
from unittest.mock import patch, MagicMock
from WebScraping import app, analizar_seguridad
import sys
import os
from selenium.webdriver.common.by import By

# Añade el directorio src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock global para chromedriver_autoinstaller
@pytest.fixture(autouse=True)
def mock_imports():
    with patch('WebScraping.chromedriver_autoinstaller') as mock_chrome:
        yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analizar_seguridad_https(mocker):
  # Configurar todos los mocks
    mocker.patch('WebScraping.chromedriver_autoinstaller.install')
    mock_urlparse = mocker.patch('urllib.parse.urlparse')
    mock_urlparse.return_value.hostname = 'example.com'
    
    # Mock del certificado SSL
    mock_ssl = mocker.patch('ssl.get_server_certificate')
    mock_ssl.return_value = "fake_cert"
    
    # Mock de OpenSSL
    mock_cert = MagicMock()
    mock_cert.get_subject.return_value.CN = "example.com"
    mocker.patch('OpenSSL.crypto.load_certificate', return_value=mock_cert)
    
    # Mock de Selenium
    mock_driver = MagicMock()
    mock_driver.get_cookies.return_value = [{'name': 'test', 'value': 'cookie_value'}]  # Cookies simuladas
    mock_driver.find_elements.side_effect = [
        [MagicMock()],  # Formularios
        [MagicMock(get_attribute=MagicMock(return_value="http://external.com/script.js"))]  # Scripts
    ]
    
    mocker.patch('WebScraping.webdriver.Chrome', return_value=mock_driver)
    mocker.patch('time.sleep')  # Mock para evitar delays reales

    # Ejecutar la función bajo prueba
    resultado = analizar_seguridad("https://example.com")
    
    # Verificaciones
    assert resultado["ssl"] is True
    assert resultado["cookies"] is False
    assert resultado["formularios"] is False
    assert resultado["scripts_externos"] is False

def test_analizar_seguridad_http(mocker):
    # Mock para Selenium
    mock_driver = MagicMock()
    mock_driver.get_cookies.return_value = []
    mock_driver.find_elements.return_value = []
    
    mocker.patch('WebScraping.webdriver.Chrome', return_value=mock_driver)
    mocker.patch('time.sleep')
    
    # Probar con URL HTTP
    url = "http://example.com"
    resultado = analizar_seguridad(url)
    
    assert resultado["ssl"] is False
    assert resultado["puntuacion"] < 100

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_post(client, mocker):
    # Mockear la función analizar_seguridad
    mocker.patch('WebScraping.analizar_seguridad', return_value={
        "ssl": True,
        "cookies": False,
        "formularios": True,
        "scripts_externos": False,
        "puntuacion": 75
    })
    
    # Mockear Selenium para el scraping
    mock_driver = MagicMock()
    mock_driver.find_elements.return_value = [
        MagicMock(text="Titulo 1"),
        MagicMock(text="Titulo 2")
    ]
    mocker.patch('WebScraping.webdriver.Chrome', return_value=mock_driver)
    
    response = client.post('/', data={'url': 'https://example.com'})
    assert response.status_code == 200
    assert b"Titulo 1" in response.data

def test_api_scrape_success(client, mocker):
    # Configurar mocks
    mocker.patch('WebScraping.analizar_seguridad', return_value={
        "ssl": True,
        "cookies": True,
        "formularios": False,
        "scripts_externos": False,
        "puntuacion": 85
    })
    
    mock_driver = MagicMock()
    mock_driver.find_elements.side_effect = [
        [MagicMock(text="Titulo 1"), MagicMock(text="Titulo 2")],  # h1, h2, h3
        [MagicMock(get_attribute=MagicMock(return_value="http://example.com/link1"))],  # enlaces
        [MagicMock(get_attribute=MagicMock(return_value="http://example.com/image1.jpg"))]  # imágenes
    ]
    mocker.patch('WebScraping.webdriver.Chrome', return_value=mock_driver)
    
    response = client.post('/api/scrape', json={'url': 'https://example.com'})
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['headings']) == 2
    assert len(data['links']) == 1
    assert len(data['images']) == 1

def test_api_scrape_invalid_url(client):
    response = client.post('/api/scrape', json={'url': ''})
    data = response.get_json()
    
    assert response.status_code == 400
    assert data['error'] == "URL is required"

def test_api_scrape_error(client, mocker):
    # Simular error en el driver
    mock_driver = MagicMock()
    mock_driver.get.side_effect = Exception("Error de conexión")
    mocker.patch('WebScraping.webdriver.Chrome', return_value=mock_driver)
    
    response = client.post('/api/scrape', json={'url': 'https://example.com'})
    data = response.get_json()
    
    assert response.status_code == 500
    assert data['success'] is False