from fastapi import FastAPI
from router.allroutes import router

app = FastAPI()

app.include_router(router)