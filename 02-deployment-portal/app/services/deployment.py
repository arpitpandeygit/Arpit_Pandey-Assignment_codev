import json
import uuid
from datetime import datetime
from pathlib import Path

DEPLOYMENTS_FILE = Path("app/state/deployments.json")

def trigger_deployment(payload: dict):
    service_name = payload["service_name"]

    deployments = json.loads(DEPLOYMENTS_FILE.read_text())

    build_id = f"build-{uuid.uuid4().hex[:8]}"

    deployments[build_id] = {
        "build_id": build_id,
        "service_name": service_name,
        "status": "QUEUED",
        "triggered_at": str(datetime.utcnow()),
        "completed_at": None
    }

    DEPLOYMENTS_FILE.write_text(json.dumps(deployments, indent=2))

    return {
        "build_id": build_id,
        "status": "QUEUED"
    }

