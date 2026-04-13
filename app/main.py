from fastapi import FastAPI

app = FastAPI(title="AI Job Tracker API")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "job-tracker"}