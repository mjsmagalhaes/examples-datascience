from fastapi.middleware.wsgi import WSGIMiddleware

from .base.app import app
from .wordcloud.app import app as wc_app, prefix as wc_prefix
from .dash_example.example import app as dex_app, prefix as dex_prefix


app.mount(wc_prefix, wc_app)
app.mount(dex_prefix, WSGIMiddleware(dex_app.server))
