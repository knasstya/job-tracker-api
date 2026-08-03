from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Job Tracker API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }