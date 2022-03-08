import tldextract as tld
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main.j2", {'request': request})


@app.post("/upload/log")
async def root(file: UploadFile = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
