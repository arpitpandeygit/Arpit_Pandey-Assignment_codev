from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.middleware.request_context import RequestContextMiddleware
from app.api.routes import router

app = FastAPI(title="User Metadata Service")

app.add_middleware(RequestContextMiddleware)

app.include_router(router)

# Prometheus metrics endpoint
app.mount("/metrics", make_asgi_app())

