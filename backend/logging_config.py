from loguru import logger

logger.add("logs.json", format="{time} {level} {message}", level="INFO", rotation="10 MB", serialize=True)

def log_request(request, response):
    logger.info(f"Request: {request.method} {request.url} - Status: {response.status_code}")
