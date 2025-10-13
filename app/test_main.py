from fastapi.testclient import TestClient
from app.main import app
import subprocess

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Security Scan" in response.text  # busca texto del HTML


def test_scan_url_success(monkeypatch):
    # Mock del subprocess.run
    cp = subprocess.CompletedProcess(
        args=["nmap"], returncode=0, stdout="Nmap done\nPORT 22 open\n", stderr=""
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: cp)

    response = client.post(
        "/api/scan", json={"scan_type": "url", "target": "scanme.nmap.org"}
    )

    # Recomendado: comprobar status
    assert response.status_code == 200

    print("\n--- DEBUG ---")
    print("response.status_code:", response.status_code)
    print("response.text:", repr(response.text))
    print("response.json():", response.json())
    # Es un JSON string, por tanto:
    data = response.json()

    print("type(data):", type(data))
    print("isinstance(data, str):", isinstance(data, str))
    print("--- END DEBUG ---\n")
    assert isinstance(data, str)
    assert "Nmap done" in data
    assert "PORT 22" in data
