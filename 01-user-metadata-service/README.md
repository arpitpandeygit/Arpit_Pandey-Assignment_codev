# User Metadata Service  
**Backend Reliability & SRE-Focused Microservice**

---

## 1. Executive Summary

This project implements a **resilient backend microservice** for managing user
metadata. The service is designed using **production-grade reliability and
observability patterns**, reflecting practices commonly used by SRE, DevOps, and
Platform Engineering teams.

The primary goal of this service is to demonstrate:

- Safe handling of retries and duplicate requests  
- Graceful behavior during downstream dependency failures  
- Clear observability signals for debugging and operations  
- Infrastructure readiness for containerized environments  

---

## 2. Problem Statement (Revisited)

The service exposes two APIs:

### API 1 — POST `/user`
Creates a new user with the following fields:
- `user_id`
- `name`
- `email`
- `phone`
- `created_at`

### API 2 — GET `/user/{id}`
Fetches previously stored user metadata.

The service satisfies **mandatory reliability
requirements**, including idempotency, retries, circuit breaking, metrics,
structured logging, and Docker-based deployment.

---

## 3. High-Level Architecture
<img width="450" height="700" alt="architecture diagram" src="https://github.com/user-attachments/assets/b15db0ab-c127-40ea-a2fc-94c6ca6ff5ed" />

Client  
→ FastAPI (API Layer)  
→ Service Layer (Idempotency, Retry with Backoff)  
→ Repository Layer (Circuit Breaker)  
→ SQLite Database  

### Cross-Cutting Concerns
- Request ID and latency tracking via middleware  
- Prometheus-compatible metrics  
- Structured JSON logging  

This layered structure enables clear separation of concerns and predictable
failure handling, which simplifies both debugging and long-term maintenance.

---

## 4. Design Philosophy (SRE Mindset)

The service is built with the assumption that:

- Networks fail  
- Clients retry requests  
- Databases may degrade temporarily  
- Debugging often happens during live incidents  

Based on these assumptions, the design prioritizes:

- **Safety over throughput**  
- **Observability over minimalism**  
- **Explicit failure handling over implicit behavior**  

---

## 5. Reliability Patterns — Deep Dive

### 5.1 Idempotency

**Problem addressed:**  
Duplicate requests caused by client retries, timeouts, or upstream replays.

**Implementation approach:**
- `user_id` is treated as a stable idempotency key  
- The database enforces uniqueness via a primary key  
- The service layer checks for an existing record before attempting a write  

**Operational impact:**
- Safe client retries  
- Exactly-once behavior at the application level  
- No duplicate data creation  

---

### 5.2 Retry with Exponential Backoff and Jitter

**Problem addressed:**  
Transient database failures such as brief lock contention or connection hiccups.

**Implementation approach:**
- Retries are applied only to database write operations  
- Retry attempts are bounded  
- Exponential backoff with jitter is used  

**Why jitter matters:**  
Without jitter, synchronized retries can overwhelm a recovering database and
amplify outages.

**Operational impact:**
- Improved resilience during short-lived incidents  
- Controlled retry behavior that respects downstream capacity  

---

### 5.3 Circuit Breaker (Database Layer)

**Problem addressed:**  
Cascading failures when a downstream dependency becomes unhealthy.

**Implementation approach:**
- Circuit breaker is applied at the repository (database access) layer  
- After a configurable number of failures, the circuit opens and fails fast  

**Operational impact:**
- Protects the database during outages  
- Preserves application resources  
- Makes failure modes explicit and observable  

---

## 6. Observability

### 6.1 Metrics (Prometheus-Compatible)

The service exposes a `/metrics` endpoint suitable for Prometheus scraping.

Tracked metrics include:
- `total_requests`  
- `success_count`  
- `failure_count`  
- `request_latency_ms` (histogram)  

These metrics support:
- Latency analysis  
- Error rate tracking  
- Traffic volume monitoring  

Metrics are exposed by the service; dashboard and alert configuration are out of
scope for this assignment.

---

### 6.2 Structured Logging

All requests emit structured JSON logs including:
- Request ID  
- Request path  
- Latency  
- Status code  
- Error summary (if applicable)  

Structured logs allow correlation across requests and services during incident
investigation.

---

## 7. Error Handling & Edge Cases

| Scenario | Behavior |
|--------|----------|
| Duplicate POST | Returns existing user (idempotent) |
| User not found | HTTP 404 |
| Transient DB error | Retry with backoff |
| Persistent DB failure | Circuit breaker opens |
| Unexpected exception | Logged with request ID |
| Service health | `/health` endpoint |

Each scenario is handled explicitly to avoid ambiguous runtime behavior.

---

## 8. Dockerization & Infrastructure Readiness

The service is packaged as a Docker image using conservative best practices:
- Slim base image  
- Non-root execution  
- Explicit health check  
- Clear port exposure  

The image is suitable for Kubernetes deployments, CI/CD pipelines, and local
development parity.

---

## 9. Running the Service

The service can be run either locally or inside a Docker container.  
Local execution is intended for development and testing, while Docker execution
ensures environment consistency and deployment readiness.

---

## 10. Operational Playbook (Excerpt)

**If latency spikes:**
- Inspect request latency metrics  
- Check database circuit breaker behavior  
- Review recent logs by request ID  

**If error rate increases:**
- Determine whether failures are client-side or database-related  
- Confirm whether retries are occurring  
- Validate circuit breaker state  

**If service is unhealthy:**
- Check `/health` endpoint  
- Review container logs and metrics  
- Restart the container if required  

These steps reflect common first-response workflows during incidents.

---

## 11. Design Trade-offs & Limitations

- SQLite is used for local testing; production deployments would use a managed database  
- Authentication and authorization are out of scope  
- Metrics dashboards and alerting rules are intentionally excluded  

These trade-offs keep the focus on reliability and operability.

---

## 12. Closing Notes

This service is intentionally focused on predictable behavior under failure. The emphasis throughout the design is on:

- Failure-aware behavior  
- Clear operational signals  
- Safe interaction with downstream dependencies  
- Ease of ownership by SRE and platform teams  

---

### Final Note

This document is written as an engineering design and operations document,
reflecting how the service would typically be discussed during design reviews,
incident analysis, and operational readiness checks.

---



