"# Health Check API

A simple FastAPI application for health check endpoints.

## Features

- **`/health`** - Basic health check with status and timestamp
- **`/health/detailed`** - Detailed health check including uptime information
- **`/docs`** - Interactive API documentation (Swagger UI)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Endpoints

- `GET /` - Root endpoint with available endpoints
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed health check with uptime
- `GET /docs` - Interactive API documentation

## Example Responses

**GET /health**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-19T10:30:45.123456"
}
```

**GET /health/detailed**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-19T10:30:45.123456",
  "uptime_seconds": 125.45,
  "service": "Health Check API"
}
```" 
