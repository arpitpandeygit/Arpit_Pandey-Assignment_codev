from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Template
from pathlib import Path

from app.api.routes import router
from app.services.health import get_service_health

app = FastAPI(title="Deployment Portal Backend")

# Include platform APIs
app.include_router(router)

# Liveness probe
@app.get("/health")
def health():
    return {"status": "ok"}

# Human-friendly dashboard (read-only)
@app.get("/dashboard/{service_name}", response_class=HTMLResponse)
def dashboard(service_name: str):
    data = get_service_health(service_name)

    template_path = Path("app/templates/dashboard.html")
    template = Template(template_path.read_text())

    return template.render(**data)

