import uvicorn
import fire

class Commands:
    pass
    
    def run(self):
        uvicorn.run("dsapps:app", port=8000, reload=True)


def cli():
    fire.Fire(Commands)