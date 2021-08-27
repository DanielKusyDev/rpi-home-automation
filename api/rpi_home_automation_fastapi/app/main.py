import uvicorn
from app.api.app import init_app
from app.config.settings import HOST, PORT

app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
