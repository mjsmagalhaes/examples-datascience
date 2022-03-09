from imp import reload
import uvicorn

uvicorn.run("dsapps:app", port=8000, reload=True)
