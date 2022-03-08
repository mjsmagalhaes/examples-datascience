from .base.app import app
from .wordcloud.app import app as app_wordcloud

app.mount("/wordcloud", app_wordcloud)
