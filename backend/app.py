from fastapi import FastAPI
from backend.routers import events

app = FastAPI(title="Cycle Planner API")

app.include_router(events.router)

@app.get("/")
def read_root():
    return {"message": "Cycle Planner API is running"}
