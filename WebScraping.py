from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

from urllib.parse import urlparse
import ssl
import OpenSSL
import time

app = Flask(__name__)

def analizar_seguridad(url):
    seguridad = {
        "ssl": False,
        "cookies": False,
        "formularios": False,
        "scripts_externos": False,
        "puntuacion": 0  # 0-100
    }

    try:
        # Verificar SSL
        if url.startswith("https://"):
            seguridad["ssl"] = True
            hostname = urlparse(url).hostname
            cert = ssl.get_server_certificate((hostname, 443))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            seguridad["puntuacion"] += 40
        else:
            seguridad["puntuacion"] -= 40

        # Configurar Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(2)
        # Cookies
        cookies = driver.get_cookies()
        if cookies:
            seguridad["cookies"] = True
            seguridad["puntuacion"] += 20
        else:
            seguridad["puntuacion"] += 10

        # Formularios
        formularios = driver.find_elements(By.TAG_NAME, "form")
        if formularios:
            seguridad["formularios"] = True
            seguridad["puntuacion"] -= 5
        else:
            seguridad["puntuacion"] += 10

        # Scripts externos
        scripts = driver.find_elements(By.TAG_NAME, "script")
        for script in scripts:
            src = script.get_attribute("src")
            if src and not urlparse(src).hostname in [urlparse(url).hostname, ""]:
                seguridad["scripts_externos"] = True
                seguridad["puntuacion"] -= 15
                break
            else:
                seguridad["puntuacion"] += 20

        driver.quit()

    except Exception as e:
        print(f"Error en análisis: {e}")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)