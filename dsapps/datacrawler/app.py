from typing import Dict
import tldextract as tld
import starlette.status as status
import os.path as path
import json
from datetime import datetime

from pathlib import Path
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from requests import get, post

from pydantic import BaseModel
from .. import BASE_DIR, templates, assets
from .keys import credentials

templates = Jinja2Templates(directory=str(assets))

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("datacrawler/index.html", {'request': request})

@app.get("/data/raids/json_output")
async def raidDataStub(character:str, realm:str):
    with open(Path(BASE_DIR, 'datacrawler/output.json')) as output:
        data:Dict = json.load(output)
    
    return data

@app.get("/data/raids")
async def raidData(character:str, realm:str):
    with open(Path(BASE_DIR, 'datacrawler/credentials.json')) as credentials_file:
        data:Dict = json.load(credentials_file)
    
    deadline = datetime.fromtimestamp( float(data.get('expiration', 0) ))
    
    if deadline < datetime.now():
        # get auth
        response = post('https://us.battle.net/oauth/token', data=credentials)
        data = response.json()
        data.update({'expiration': datetime.now().timestamp() + int(data['expires_in'])})
        print(data)

        with open(Path(BASE_DIR, 'datacrawler/credentials.json'), 'w') as credentials_file:
            json.dump(data, credentials_file)
        
        data.update({'status': 'Renewed.'})
    else:
        data.update({'status': 'Skipped Auth.'})
    
    url = f'https://us.api.blizzard.com/profile/wow/character/{realm}/{character}/encounters/raids'

    response = get(url, params={
        'namespace': 'profile-us',
        'locale':'en_US',
        'access_token': data['access_token']
    })

    # return {
    #     'url': response.url,
    #     'headers': response.headers,
    #     'content': response.content,
    #     'json': response.status_code,
    #     'data': data
    # }

    return response.json()
    
