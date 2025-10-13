from fastapi.testclient import TestClient
from app.main import app
import subprocess

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Security Scan" in response.text  # busca texto del HTML


def test_scan_url_success(monkeypatch):
    # Simula un subprocess.run exitoso
    cp = subprocess.CompletedProcess(
        args=["nmap"], returncode=0, stdout="Nmap done\nPORT 22 open\n", stderr=""
    )
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: cp)

    response = client.post(
        "/api/scan", data={"scan_type": "url", "target": "scanme.nmap.org"}
    )
    assert response.status_code == 200
    # Como la vista devuelve HTML, miramos response.text
    assert "Nmap done" in response.text
    assert "url" in response.text and "scanme.nmap.org" in response.text
