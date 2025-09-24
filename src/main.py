from fastapi import FastAPI
import uvicorn
from src.routes import offers
from src.middleware.rate_limiter import RateLimiterMiddleware

app = FastAPI(title="Holiday Finder API", version="0.1.0")

# Add rate limiting middleware (20 requests per minute per IP)
app.add_middleware(RateLimiterMiddleware, calls=20, period=60)

app.include_router(offers.router, prefix="/api", tags=["offers"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
