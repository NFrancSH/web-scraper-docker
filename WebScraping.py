from flask import Flask, request, jsonify  # Cambiamos render_template por jsonify
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from flask_cors import CORS
import chromedriver_autoinstaller
from OpenSSL import crypto
import re

from urllib.parse import urlparse
import ssl
import time

app = Flask(__name__)
CORS(app)  # Añade esto después de crear la app

# O para más control:
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Permite todos los orígenes
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

app = Flask(__name__)

def validar_url(url: str) -> bool:
    """Valida estructuralmente una URL antes de procesarla"""
    if not isinstance(url, str):
        raise ValueError("La URL debe ser un string")
    
    if len(url) > 500:
        raise ValueError("URL excede longitud máxima (500 caracteres)")
    
    # Patrón para evitar XSS e inyecciones
    patron_seguro = re.compile(
        r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        r'(?::\d+)?(?:/[-\w._~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    
    if not patron_seguro.match(url):
        raise ValueError("URL contiene caracteres o patrones potencialmente peligrosos")
    
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError("URL no válida: falta esquema o dominio")
    
    return True

def analizar_seguridad(url):
    # Validación de URL
    """Analiza la seguridad de una URL.
    
    Args:
        url (str): URL a analizar (debe comenzar con http:// o https://)
    
    Returns:
        dict: Resultados del análisis
    
    Raises:
        ValueError: Si la URL no es válida
    """
    try:
        validar_url(url)  # Validación estricta primero
    except ValueError as e:
        raise  # Relanzar para que lo capture pytest.raises
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"URL no válida: '{url}'. Debe incluir esquema (http/https) y dominio")
    
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Esquema no soportado: '{parsed.scheme}'. Use (http:// o https://)")

    seguridad = {
        "ssl": False,
        "certificado": None,  # Añadido para la prueba
        "cookies": False,
        "formularios": False,
        "scripts_externos": False,
        "puntuacion": 0,
        "error": None  # Para manejar errores
    }

    driver = None
    try:
        # Verificar SSL
        if url.startswith("https://"):
            hostname = urlparse(url).hostname
            cert_pem = ssl.get_server_certificate((hostname, 443))
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
            seguridad["ssl"] = True
            seguridad["certificado"] = {
                "emisor": cert.get_issuer().CN,
                "valido_hasta": cert.get_notAfter().decode("utf-8"),
            }
            seguridad["puntuacion"] += 40
        else:
            seguridad["puntuacion"] = max(0, seguridad["puntuacion"] - 10)  # Evita negativos

        # Configurar Selenium
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chromedriver_autoinstaller.install()
        driver = Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(2)

        # Cookies
        cookies = driver.get_cookies()
        seguridad["cookies"] = len(cookies) > 0  # True si hay cookies
        seguridad["puntuacion"] += 20 if cookies else 10

        # Formularios
        formularios = driver.find_elements(By.TAG_NAME, "form")
        seguridad["formularios"] = bool(formularios)
        seguridad["puntuacion"] += 20 if not formularios else 10

        # Scripts externos
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            src = script.get_attribute("src")
            if src and urlparse(src).hostname not in [hostname, None]:
                seguridad["scripts_externos"] = True
                break
        seguridad["puntuacion"] += 20 if not seguridad["scripts_externos"] else -10

    except Exception as e:
        seguridad["error"] = str(e)
    finally:
        if driver:
            driver.quit()

    return seguridad

@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    url_ingresada = None
    seguridad = None

    if request.method == "POST":
        url_ingresada = request.form["url"]
        seguridad = analizar_seguridad(url_ingresada)

        # Scraping básico de títulos
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)

        
        try:
            driver.get(url_ingresada)
            time.sleep(2)
            elementos = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
            resultados = [e.text for e in elementos if e.text.strip()]
        except Exception as e:
            resultados = [f"Error: {str(e)}"]
        finally:
            driver.quit()

    return render_template(
        "index.html",
        resultados=resultados,
        url=url_ingresada,
        seguridad=seguridad
    )

# WebScraping.py (modificaciones)
@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    
    try:
        # Análisis de seguridad
        seguridad = analizar_seguridad(url)
        
        # Scraping de contenido
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        time.sleep(2)
        
        # Obtener más datos
        titulos = [e.text for e in driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3") if e.text.strip()]
        enlaces = [e.get_attribute('href') for e in driver.find_elements(By.TAG_NAME, "a") if e.get_attribute('href')]
        imagenes = [e.get_attribute('src') for e in driver.find_elements(By.TAG_NAME, "img") if e.get_attribute('src')]
        
        driver.quit()
        
        return jsonify({
            "success": True,
            "url": url,
            "security": seguridad,
            "headings": titulos,
            "links": enlaces[:20],  # Limitar cantidad
            "images": imagenes[:10]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Error al analizar la URL"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)