import time
from collections import defaultdict, deque
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 20, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Clean old entries
        while (
            self.clients[client_ip] and self.clients[client_ip][0] <= now - self.period
        ):
            self.clients[client_ip].popleft()

        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            return JSONResponse(
                status_code=429,
                content={"detail": f"Rate limit exceeded: {self.calls} requests per {self.period} seconds"}
            )

        # Add current request
        self.clients[client_ip].append(now)

        # Process request
        response = await call_next(request)
        return response
