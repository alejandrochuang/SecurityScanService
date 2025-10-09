from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import subprocess

app = FastAPI()

class Item(BaseModel):
    text: str 
    is_done: bool = False

items = []

@app.post("/scan/{scan_id}")
def scan(scan_id: str) -> Dict[str,str]:
    print("hola")
    if (scan_id=="url"):
        result = subprocess.run(
            ["nmap", "scanme.nmap.org"],
            capture_output=True,
            text=True,
            timeout=100
        )
        return {"output": result.stdout}
    elif (scan_id=="docker"):
        print("docker")
    else:
        raise HTTPException(status_code=404, detail="scan not available")


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int)  -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")