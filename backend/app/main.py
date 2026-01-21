"""
FastAPI application entry point.
Configures the app, initializes database, and registers routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.db import init_db_pool, create_tables, close_db_pool
from app.routes import auth_routes, dataset_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting application...")
    
    try:
        # Initialize database connection pool
        init_db_pool(min_conn=2, max_conn=10)
        
        # Create database tables if they don't exist
        create_tables()
        
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    close_db_pool()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Multi-User Dataset Management Platform",
    description="Backend API for managing datasets with JWT authentication and role-based access control",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration - adjust for production
aapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(auth_routes.router)
app.include_router(dataset_routes.router)


@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint.
    Returns basic API information.
    """
    return {
        "status": "online",
        "service": "Multi-User Dataset Management Platform",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint.
    Can be extended to check database connectivity.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # In production, use a production ASGI server with proper configuration
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Disable in production
        log_level="info"
    )
