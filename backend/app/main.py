"""FastAPI Main Application Module."""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import SkylarkBIException
from app.api.routes.query import router as query_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Conversational AI Business Intelligence Agent for Skylark Drones",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(query_router)


@app.exception_handler(SkylarkBIException)
async def skylark_exception_handler(request: Request, exc: SkylarkBIException):
    """Centralized exception handler for custom application exceptions."""
    logger.error(f"Application error: {exc.message} | Details: {exc.details}")
    return JSONResponse(
        status_code=400,
        content={"error": exc.message, "details": exc.details}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global fallback exception handler suppressing internal stack traces."""
    logger.error(f"Unhandled server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "An internal server error occurred. Please try again later."}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint returning service connectivity status."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENV,
        "monday_api_configured": settings.is_monday_configured,
        "gemini_api_configured": settings.is_gemini_configured,
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
