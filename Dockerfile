FROM python:3.11-slim

# SO deps (light) + cleanup
RUN apt update \
    && apt install -y --no-install-recommends nmap curl ca-certificates tar \
    && rm -rf /var/lib/apt/lists/*

# Trivy (official installation; without sudo)
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
    | sh -s -- -b /usr/local/bin v0.67.0

WORKDIR /app 

# Installs Python dependencies (does not use cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installs Python deps for development environment (does not use cache)
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copies code
COPY . /app

EXPOSE 8000

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

