import tldextract as tld
import string
import random
import starlette.status as status
import os
import os.path as path

from pathlib import Path
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from wordcloud import WordCloud
from tempfile import mkstemp

from pydantic import BaseModel
from .. import BASE_DIR, templates, assets


class Text(BaseModel):
    text: str


templates = Jinja2Templates(directory=str(assets))

static = Path(BASE_DIR, '_images')
# static = Path(BASE_DIR, '_images').relative_to(path.abspath(path.curdir))

if not static.exists():
    os.mkdir(static)

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(static)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("wordcloud/index.html", {'request': request})


@app.post("/")
async def generate_image(request: Request, data: Text):
    wc = WordCloud().generate(data.text)
    filename = 'tmp_' + \
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

    wc.to_file(Path(static, filename+'.jpg').as_posix())

    return {
        'filename': '/wordcloud/'+filename,
        'path': "/wordcloud/static/"+filename+'.jpg'
    }


@app.get("/{filename}")
async def root(request: Request, filename):
    return templates.TemplateResponse("wordcloud/index.html", {
        'request': request,
        'filename': '/wordcloud/'+filename,
        'path': "/wordcloud/static/"+filename+'.jpg'
    })
