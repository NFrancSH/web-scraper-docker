# Usa una imagen base con Python
FROM python:3.9-slim

# Instala dependencias del sistema + agrega repositorio oficial de Google Chrome
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget curl gnupg unzip && \
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# # Descarga y configura chromedriver (compatible con la versión de Chrome instalada)
# RUN LATEST_CHROME_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
#     wget -q https://chromedriver.storage.googleapis.com/$LATEST_CHROME_VERSION/chromedriver_linux64.zip && \
#     unzip chromedriver_linux64.zip -d /usr/bin/ && \
#     rm chromedriver_linux64.zip && \
#     chmod +x /usr/bin/chromedriver

# Instala Chrome y dependencias de sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    unzip \
    python3-dev \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 && \
    wget -q -O /usr/share/keyrings/google-chrome.gpg https://dl.google.com/linux/linux_signing_key.pub && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*




# Configura el entorno
WORKDIR /app
COPY . .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto expuesto
EXPOSE 5000

# Comando de inicio
CMD ["python", "WebScraping.py"]
