from WebScraping import  analizar_seguridad
import pytest
import ssl
import time
import statistics
import concurrent.futures

def test_rendimiento_analisis():
    URL_TEST = "https://example.com"
    NUM_REQUESTS = 50  # Número de ejecuciones concurrentes
    tiempos = []
    
    def ejecutar_analisis():
        inicio = time.time()
        analizar_seguridad(URL_TEST)
        return time.time() - inicio

    # Ejecución secuencial para diagnóstico
    for _ in range(NUM_REQUESTS):
        tiempos.append(ejecutar_analisis())
    
    print(f"\nResultados ({NUM_REQUESTS} ejecuciones):")
    print(f"Tiempo promedio: {statistics.mean(tiempos):.2f}s")
    print(f"Tiempo máximo: {max(tiempos):.2f}s")
    print(f"Desviación estándar: {statistics.stdev(tiempos):.2f}s")
    
    assert statistics.mean(tiempos) < 50.0  # Umbral aceptable

def test_escalabilidad_paralela():
    URLs = [
        "https://example.com",
        "https://google.com",
        "https://github.com"
    ] * 10  # 30 URLs
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(analizar_seguridad, URLs))
    
    assert all(r["ssl"] is True for r in resultados)  # Todas deben completarse

def test_estabilidad_larga_duracion():
   for i in range(100):  # 100 iteraciones
        resultado = analizar_seguridad("https://example.com")
        assert resultado["ssl"] is True
        if i % 10 == 0:
            print(f"Iteración {i}: OK")

@pytest.mark.parametrize("url_invalida", [
    "javascript:alert(1)",
    "http://<script>alert('XSS')</script>",
    "https://" + "a" * 1000 + ".com"
])
def test_seguridad_inputs_maliciosos(url_invalida):
    with pytest.raises((ValueError, ssl.SSLError)):
        analizar_seguridad(url_invalida)

@pytest.mark.parametrize("chrome_version", ["115", "120", "stable"])
def test_compatibilidad_chromedriver(mocker, chrome_version):
    mocker.patch('chromedriver_autoinstaller.get_chrome_version', return_value=chrome_version)
    resultado = analizar_seguridad("https://example.com")
    assert resultado["ssl"] is True