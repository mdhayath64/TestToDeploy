from fastapi import FastAPI
from datetime import datetime
import time

app = FastAPI(title="Health Check API")

# Track application start time
start_time = time.time()

@app.get("/health")
def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health/detailed")
def detailed_health_check():
    """Detailed health check with uptime information"""
    uptime = time.time() - start_time
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": uptime,
        "service": "Health Check API"
    }

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Health Check API is running",
        "endpoints": {
            "health": "/health",
            "detailed": "/health/detailed",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
