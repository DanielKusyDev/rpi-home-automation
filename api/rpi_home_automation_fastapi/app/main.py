import uvicorn
from app.api.app import init_app
from app.config.settings import HOST, PORT, RPI_ENABLED

app = init_app()

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    finally:
        if RPI_ENABLED:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
