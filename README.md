# 🕸 Web Scraper Dockerizado

Este proyecto es una aplicación Flask que analiza sitios web usando Selenium y Google Chrome sin interfaz gráfica, todo dentro de un contenedor Docker.

---

## 🚀 Características

- Scraping básico de encabezados
- Análisis de seguridad:
  - SSL habilitado
  - Cookies detectadas
  - Formularios presentes
  - Scripts externos
- Dockerizado para fácil ejecución
- Compatible con cualquier sistema operativo con Docker

---

## 🧰 Requisitos previos

- Docker instalado: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Docker Compose

---

## 🗂 Estructura del proyecto
web-scraper-docker/
├── Dockerfile
├── docker-compose.yml
├── WebScraping.py
├── templates/
│ └── index.html
├── requirements.txt
└── README.md 
---

## ⚙ Instalación y ejecución

1. *Clona el repositorio*

```bash
git clone https://github.com/tu-usuario/web-scraper-docker.git
cd web-scraper-docker
```
> 💡 *Nota:* Si se necesita reconstruir la imagen desde 0 utilizar el paso 2

2. *Construir la imagen Docker*
```bash
docker-compose build --no-cache
```
3. *Iniciar la aplicación*
```bash
docker-compose up
```

4. *Abrir el navegador*
```bash
http://localhost:5000
```
> 💡 *Nota:* Si se quiere detener la aplicacion usar
```bash
docker-compose down
```


