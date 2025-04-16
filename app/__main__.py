import uvicorn
from config import config
import main

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.get("FastAPI")['host'],
        port=config.get("FastAPI")['port'],
        reload=config.get("FastAPI")['reload'],
        ssl_certfile=config.get("FastAPI").get("ssl_certfile"),
        ssl_keyfile=config.get("FastAPI").get("ssl_keyfile"),
    )
