from fastapi import FastAPI
from routes import subjects

app = FastAPI(title="Gamified Learning API")

# Register route group
app.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])

@app.get("/")
def root():
    return {"message": "API is running!"}
