# app/main.py
import logging

logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    response = await call_next(request)
    logger.info(f"Request: {request.method} {request.url} Status: {response.status_code}")
    return response
