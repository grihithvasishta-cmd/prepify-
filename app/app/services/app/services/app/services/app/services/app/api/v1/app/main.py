from fastapi import FastAPI
from app.api.v1 import endpoints
from app.core.database import engine, Base

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Prepify AI",
    description="AI-Powered Exam Preparation Backend",
    version="1.0.0"
)

app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "Prepify AI is running"}
