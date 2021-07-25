from fastapi import FastAPI

from routes import setup_routes
from services.db import DB

app = FastAPI()
setup_routes(app)


@app.on_event("startup")
async def startup() -> None:
    await DB.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await DB.close()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
