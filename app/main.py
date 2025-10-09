from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

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
    allowed_targets = {
        "url": ["scanme.nmap.org"],
        "docker": ["ubuntu:latest"]
    }

    # Si el tipo no existe o el target no está en la lista → error
    if target not in allowed_targets.get(scan_type, []):
        raise HTTPException(status_code=400, detail="Target no permitido")
    
    print("target ok")

    if scan_type == "url":
        print("escaneando url")
        result = subprocess.run(
            ["nmap", target],
            capture_output=True,
            text=True,
            timeout=100
        )
        output = result.stdout
    
    elif scan_type == "docker":
        print("inspeccionando container")
        result = subprocess.run(
            ["trivy","image", target],
            capture_output=True,
            text=True,
            timeout=100
        )
        output = result.stdout
    else:
        print("tipo de escaneo no válido!")
        raise HTTPException(status_code=400, detail="scan_type no válido!")


    return templates.TemplateResponse(
        "index.html",
        {"request": request, "output": output, "scan_type": scan_type, "target": target},
    )