from fastapi import FastAPI
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.profile import router as profile_router
from app.api.jobs import router as job_router
app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(profile_router)
app.include_router(job_router)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API is running"}