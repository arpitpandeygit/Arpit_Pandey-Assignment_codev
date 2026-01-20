from fastapi import APIRouter
from app.services.registration import register_service
from app.services.deployment import trigger_deployment
from app.services.health import get_service_health

router = APIRouter(prefix="/platform")

@router.post("/services")
def register(payload: dict):
    return register_service(payload)


@router.post("/deployments")
def deploy(payload: dict):
    return trigger_deployment(payload)

@router.get("/services/{service_name}/health")
def service_health(service_name: str):
    return get_service_health(service_name)
