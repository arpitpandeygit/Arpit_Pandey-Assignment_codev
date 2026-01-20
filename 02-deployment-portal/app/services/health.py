import json
from pathlib import Path

SERVICES_FILE = Path("app/state/services.json")
DEPLOYMENTS_FILE = Path("app/state/deployments.json")

def get_service_health(service_name: str):
    services = json.loads(SERVICES_FILE.read_text())
    deployments = json.loads(DEPLOYMENTS_FILE.read_text())

    if service_name not in services:
        return {"error": "Service not found"}

    service_deployments = [
        d for d in deployments.values()
        if d["service_name"] == service_name
    ]

    latest = (
        sorted(
            service_deployments,
            key=lambda x: x["triggered_at"],
            reverse=True
        )[0]
        if service_deployments else None
    )

    return {
        "service_name": service_name,
        "last_deployment_time": latest["triggered_at"]
        if latest else None,
        "deployment_status": latest["status"]
        if latest else "NOT_DEPLOYED",
        "pod_count": 3,
        "cpu_usage": "120m",
        "memory_usage": "256Mi"
    }

