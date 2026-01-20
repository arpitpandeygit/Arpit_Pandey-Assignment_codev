import json
from datetime import datetime
from pathlib import Path
from jinja2 import Template

STATE_FILE = Path("app/state/services.json")

TF_ENV_ROOT = Path("terraform/envs/dev")
TF_TEMPLATE = Path("app/templates/terraform/service.tf.j2")
TF_OUTPUT_TEMPLATE = Path("app/templates/terraform/outputs.tf.j2")

K8S_TEMPLATE = Path("app/templates/kubernetes/deployment.yaml.j2")
JENKINS_TEMPLATE = Path("app/templates/jenkins/Jenkinsfile.j2")

def register_service(payload: dict):
    service_name = payload["service_name"]
    team_name = payload["team_name"]
    repo_url = payload["repo_url"]

    services = json.loads(STATE_FILE.read_text())

    if service_name in services:
        return {"error": "Service already registered"}

    # 1️⃣ Generate Terraform env
    service_tf_dir = TF_ENV_ROOT / service_name
    service_tf_dir.mkdir(parents=True, exist_ok=True)

    (service_tf_dir / "main.tf").write_text(
        Template(TF_TEMPLATE.read_text()).render(service_name=service_name)
    )
    (service_tf_dir / "outputs.tf").write_text(
        Template(TF_OUTPUT_TEMPLATE.read_text()).render(service_name=service_name)
    )

    # 2️⃣ Generate Kubernetes manifest
    k8s_out = Path("app/templates/kubernetes/generated")
    k8s_out.mkdir(exist_ok=True)

    (k8s_out / f"{service_name}-deployment.yaml").write_text(
        Template(K8S_TEMPLATE.read_text()).render(
            service_name=service_name,
            team_name=team_name,
            image="REPLACE_WITH_ECR_IMAGE"
        )
    )

    # 3️⃣ Generate Jenkinsfile
    ci_out = Path("app/templates/jenkins/generated")
    ci_out.mkdir(exist_ok=True)

    (ci_out / f"{service_name}.Jenkinsfile").write_text(
        Template(JENKINS_TEMPLATE.read_text()).render(service_name=service_name)
    )

    # 4️⃣ Persist metadata
    services[service_name] = {
        "service_name": service_name,
        "team_name": team_name,
        "repo_url": repo_url,
        "registered_at": str(datetime.utcnow())
    }

    STATE_FILE.write_text(json.dumps(services, indent=2))

    return {
        "service_name": service_name,
        "status": "REGISTERED",
        "artifacts": {
            "terraform": str(service_tf_dir),
            "k8s_manifest": str(k8s_out),
            "jenkins_pipeline": str(ci_out)
        }
    }

