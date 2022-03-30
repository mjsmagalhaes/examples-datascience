from fastapi.middleware.wsgi import WSGIMiddleware

from .app import app, BASE_DIR, templates, assets
from .wordcloud.app import app as wc_app, prefix as wc_prefix
from .dash_example.example import app as dex_app, prefix as dex_prefix
from .datacrawler.app import app as dc_app

app.mount(wc_prefix, wc_app)
app.mount(dex_prefix, WSGIMiddleware(dex_app.server))
app.mount("/datacrawler", dc_app)