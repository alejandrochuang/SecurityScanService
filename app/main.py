from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess


class ScanRequest(BaseModel):
    scan_type: str
    target: str


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


class ScanRequest(BaseModel):
    scan_type: str
    target: str


def scan_url(target) -> str:
    print("escaneando url")
    try:
        result = subprocess.run(
            [
                "nmap",
                "-sT",
                "--top-ports",
                "500",
                "-Pn",
                "-T4",
                "--max-retries",
                "1",
                "-A",
                "--host-timeout",
                "45s",
                target,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout
        return output
    except subprocess.TimeoutExpired:
        print("excepción timeout?")
        raise HTTPException(
            status_code=504,
            detail="Timeout: el escaneo tardó más de {}s".format(max_timeout),
        )


def scan_image(name) -> str:
    print("inspeccionando imagen")
    try:
        result = subprocess.run(
            ["trivy", "image", target],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout
        return output
    except subprocess.TimeoutExpired:
        print("excepción timeout?")
        raise HTTPException(
            status_code=504,
            detail="Timeout: el escaneo tardó más de {}s".format(max_timeout),
        )


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ui/scan", response_class=HTMLResponse)
def ui_scan(
    request: Request,
    scan_type: str = Form(...),
    target: str = Form(...),
):
    # --- VALIDACIÓN ---
    allowed_targets = {"url": ["scanme.nmap.org"], "docker": ["ubuntu:latest"]}
    print("validamos")
    print("target =", target)
    # Si el tipo no existe o el target no está en la lista → error
    if target not in allowed_targets.get(scan_type, []):
        raise HTTPException(status_code=400, detail="Target no permitido")

    print("target ok")
    if scan_type == "url":
        output = scan_url(target)

    elif scan_type == "docker":
        output = scan_image(target)
    else:
        print("tipo de escaneo no válido!")
        raise HTTPException(status_code=400, detail="scan_type no válido!")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "output": output,
            "scan_type": scan_type,
            "target": target,
        },
    )


@app.post("/api/scan", response_class=JSONResponse)
def api_scan(scan: ScanRequest):
    print("hola??")
    if scan.scan_type == "url":
        result = scan_url(scan.target)
    elif scan.scan_type == "docker":
        result = scan_image(scan.target)
    else:
        print("tipo de escaneo no válido!")
        raise HTTPException(status_code=400, detail="scan_type no válido")
    return result
