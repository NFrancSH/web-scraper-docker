import pytest
from WebScraping import analizar_seguridad

def test_analizar_seguridad_https_caja_negra():
    # Caso 1: URL con HTTPS válido (simulado)
    resultado = analizar_seguridad("https://example.com")
    assert isinstance(resultado, dict)
    assert "certificado" in resultado
    assert "cookies" in resultado
    assert "scripts_externos" in resultado

    # Caso 2: URL sin HTTPS (debería fallar o manejarse)
    resultado_http = analizar_seguridad("http://insecure.com")
    assert resultado_http["ssl"] is False
    assert resultado_http["puntuacion"] < 40

    # Caso 3: URL inválida
    with pytest.raises(ValueError) as excinfo:
        analizar_seguridad("esto_no_es_una_url")
        assert "URL no válida" in str(excinfo.value)
    
    # Caso 4: URL sin esquema
    with pytest.raises(ValueError):
        analizar_seguridad("example.com")
    
    # Caso 5: Esquema no soportado
    with pytest.raises(ValueError):
        analizar_seguridad("ftp://example.com")

def test_url_insegura():
    resultado = analizar_seguridad("http://insecure.com")
    assert resultado["ssl"] is False
    assert resultado["puntuacion"] < 40  # Verifica la penalización