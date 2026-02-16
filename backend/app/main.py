from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.infrastructure.database import engine
from app.domain.models import Base
import time
from sqlalchemy.exc import OperationalError

app = FastAPI(title="SmartPrice API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def wait_for_db():
    for _ in range(10):
        try:
            with engine.connect():
                return
        except OperationalError:
            time.sleep(3)
    raise Exception("Banco de dados não está pronto")

@app.on_event("startup")
def on_startup():
    wait_for_db()
    Base.metadata.create_all(bind=engine)
