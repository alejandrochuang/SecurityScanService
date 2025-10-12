FROM python:3.11-slim

# SO deps (ligero) + limpieza
RUN apt update \
    && apt install -y --no-install-recommends nmap curl ca-certificates tar \
    && rm -rf /var/lib/apt/lists/*

# Trivy (instalador oficial; sin sudo)
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
    | sh -s -- -b /usr/local/bin v0.67.0

WORKDIR /app 

# Instala deps Python (aprovecha caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . /app

EXPOSE 8000

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

