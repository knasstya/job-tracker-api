from fastapi import FastAPI

from app.routers import job_router


app = FastAPI()


app.include_router(job_router.router)


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