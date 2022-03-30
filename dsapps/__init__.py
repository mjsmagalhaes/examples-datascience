from fastapi.middleware.wsgi import WSGIMiddleware

from .app import app, BASE_DIR, templates, assets
from .wordcloud.app import app as wc_app
from .dash_example.example import app as dex_app
from .datacrawler.app import app as dc_app

app.mount('/wordcloud', wc_app)
app.mount('/dash', WSGIMiddleware(dex_app.server))
app.mount('/datacrawler', dc_app)