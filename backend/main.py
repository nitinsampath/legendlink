from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.config import settings
from app.db import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Allow React frontend to talk to this backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # React app address
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.routes.files import router as files_router

    app.include_router(files_router, prefix="/api/v1/files", tags=["files"])

    return app


app = get_application()


@app.get("/")
async def root():
    return {"message": "LegendLink API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
