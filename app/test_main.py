from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Security Scan" in response.text  # busca texto del HTML


"""
def test_scan_URL():
    response = client.post("/api/scan", data={"scan_type": "url", "target": "scanme.nmap.org"})
    """
