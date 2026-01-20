# Deployment Portal Backend

**Platform Engineering / IDP / CI-CD Automation Prototype**

---

## 1. Overview

This repository implements a **self-service Deployment Portal Backend**, designed as a lightweight **Internal Developer Platform (IDP)** control plane.

The system enables application teams to:

- Register new microservices
    
- Receive standardized infrastructure and delivery contracts
    
- Trigger deployment workflows (simulated)
    
- Observe service health via a centralized platform view
    

The focus of this implementation is **platform correctness, reliability, and operability**.

The design intentionally mirrors how **SRE, Platform Engineering, and DevOps teams** structure internal systems in large organizations.

---

## 2. Problem Context

Modern engineering organizations separate responsibilities as follows:

- **Application teams** focus on business logic
    
- **Platform teams** provide paved paths for:
    
    - Infrastructure provisioning
        
    - CI/CD pipelines
        
    - Runtime standards
        
    - Operational visibility
        

This project models such a platform by exposing a **control-plane API** that orchestrates:

- Infrastructure contracts (Terraform)
    
- Runtime contracts (Kubernetes manifests)
    
- Delivery contracts (CI/CD pipelines)
    

No infrastructure is applied automatically; instead, **artifacts are generated deterministically**, allowing safe review, approval, and execution by downstream systems.

---

## 3. High-Level Architecture

<img width="880" height="553" alt="Asdakkk" src="https://github.com/user-attachments/assets/23a2482d-c622-434f-8d43-c9ef9796e533" />

**Key design principle**:

> The platform records **intent and contracts**, not execution.

---

## 4. Feature 1 — Register a New Microservice

### API

```
POST /platform/services
```

### Input

```
{
  "service_name": "payments",
  "team_name": "core-platform",
  "repo_url": "https://github.com/org/payments"
}
```

### What happens during registration

Service registration is treated as an **onboarding workflow**.

The platform automatically generates:

#### 1. Terraform Infrastructure Contracts

```
terraform/envs/dev/payments/
├── main.tf
└── outputs.tf
```

These files wire reusable Terraform modules:

- ECR repository
    
- IAM role (service-scoped, least privilege intent)
    

This mirrors real-world platform behavior where:

- Modules are owned by the platform
    
- Environment instantiations are generated per service
    

#### 2. Kubernetes Deployment Manifest (Template-Based)

```
app/templates/kubernetes/generated/payments-deployment.yaml
```

The manifest includes:

- Standard labels
    
- Resource requests and limits
    
- Team ownership metadata
    

The platform enforces runtime consistency without applying manifests directly.

#### 3. CI/CD Pipeline (Jenkinsfile)

```
app/templates/jenkins/generated/payments.Jenkinsfile
```

The pipeline defines:

- Build
    
- Test
    
- Docker build & push
    
- Deploy stages (simulated)
    

The pipeline is intentionally generic and templated to remain reusable across services.

#### 4. Metadata Persistence

```
app/state/services.json
```

This acts as the platform’s source of truth for:

- Ownership
    
- Registration timestamp
    
- Repository mapping
    

### Response

```
{
  "service_name": "payments",
  "status": "REGISTERED",
  "artifacts": {
    "terraform": "terraform/envs/dev/payments",
    "k8s_manifest": "app/templates/kubernetes/generated",
    "jenkins_pipeline": "app/templates/jenkins/generated"
  }
}
```
---

## 5. Feature 2 — Trigger a Deployment Job (Simulation)

### API

```
POST /platform/deployments
```
### Input

```
{
  "service_name": "payments"
}
```
### Behavior

This endpoint **does not invoke Jenkins directly**.

Instead, it:

- Records deployment intent
    
- Generates a unique `build_id`
    
- Stores lifecycle state in the platform
    

Initial state:

`QUEUED`

State transitions are modeled as:

`QUEUED → RUNNING → SUCCESS | FAILED`

### Why simulation?

In production environments:

- CI execution is owned by Jenkins/GitLab
    
- Platforms should not block on pipeline execution
    
- Tight coupling creates failure amplification
    

---

## 6. Feature 3 — Health Dashboard

### API

```
GET /platform/services/{service_name}/health
```
### Response

```
{
  "service_name": "payments",
  "last_deployment_time": "...",
  "deployment_status": "QUEUED",
  "pod_count": 3,
  "cpu_usage": "120m",
  "memory_usage": "256Mi"
}
```
### Notes

- Deployment data is derived from platform state
    
- Runtime metrics are **static mocks**, as allowed
    
- No Kubernetes or Prometheus dependency is introduced
    

This aligns with how internal platforms:

- Aggregate known signals
    
- Avoid tight coupling to live infrastructure
    

### Optional Dashboard UI

A minimal HTML dashboard is provided at:

`/dashboard/{service_name}`

This is a **read-only operator view**, complementing JSON APIs used by automation.

---

## 7. API Specification

The platform exposes an OpenAPI contract via FastAPI.

- Interactive docs: `/docs`
    
- Exported spec: `openapi.yaml`
    

This ensures:

- API discoverability
    
- Tooling integration
    
- Contract clarity
    

---

## 8. Terraform Design

### Structure

```
terraform/
├── modules/
│   ├── ecr/
│   ├── iam/
│   └── service/
└── envs/
    └── dev/
```
### Design Decisions

- Modules are reusable and platform-owned
    
- Each service gets its own environment instantiation
    
- IAM intent follows least-privilege principles
    

This mirrors how infra is typically gated by:

- Code review
    
- Change management
    
- CI pipelines
    

---

## 9. Security Considerations

- IAM roles are scoped per service
    
- No wildcard permissions are shown
    
- No secrets are embedded in pipelines
    
- CI/CD and infra concerns are decoupled
    
---

## 10. Operational Considerations

### Platform Responsibilities

- Contract generation
    
- State persistence
    
- API availability
    

### External Responsibilities

- Terraform execution
    
- CI pipeline execution
    
- Runtime observability
    

This separation reduces blast radius and improves ownership clarity.

---

## 11. Trade-offs and Limitations

- JSON files are used instead of a database for simplicity
    
- Deployment execution is simulated
    
- Metrics are mocked
    
- Authentication/authorization is out of scope
    

These trade-offs are intentional to keep the focus on:

- Platform design
    
- Infrastructure automation patterns
    
- CI/CD modeling
    

---

## 12. How This Would Scale in Production

In a real deployment:

- JSON state would move to a database
    
- Terraform execution would be triggered via CI
    
- Jenkins pipelines would consume platform-generated artifacts
    
- Observability would integrate with Prometheus/Grafana
    

The current design allows these evolutions without architectural changes.

---

## 13. Closing Notes

This repository demonstrates a practical approach to building an internal  
deployment platform with a strong emphasis on:

- Clear separation of responsibilities
    
- Infrastructure and delivery standardization
    
- Reusable automation primitives
    
- Operational visibility for platform and SRE teams
    

The implementation prioritizes correctness, clarity, and maintainability over  
excessive abstraction. All components are designed to be easily extended or  
integrated into a larger CI/CD and infrastructure ecosystem.
