import os
import os.path as path

import tldextract as tld

from pathlib import Path
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
# BASE_DIR = ''
assets = Path(BASE_DIR, 'dist/prod')

if not assets.exists():
    os.mkdir(assets)

templates = Jinja2Templates(directory=str(assets))

app = FastAPI()
app.mount("/assets", StaticFiles(directory=str(assets)), name="assets")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@app.post("/upload/log")
async def root(file: UploadFile = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        with file.file as f:
            print(f.readlines())

        return {"filename": file.filename}


@app.post("/upload/encounter")
async def create_encounter(file: UploadFile = None):
    pass
