# SLO Requirements
## Kubernetes, Observability & SLO Implementation

#### Production-Grade Deployment of a Sample Application

---

## 1. Overview

This assignment demonstrates the deployment and operation of a **stateless HTTP application** on Kubernetes using **production-grade standards** commonly applied in EKS-based environments.

The implementation focuses on:

- correct usage of Kubernetes primitives
    
- operational safety during scaling and disruptions
    
- observability through metrics, logs, and traces
    
- explicit reliability targets defined via Service Level Objectives (SLOs)
    

The deployed application is **NGINX**, selected intentionally as a representative production workload:

- stateless
    
- HTTP-based
    
- predictable behavior
    
- widely used in real systems
    

The goal is focused on **infrastructure correctness, operability, and reliability engineering discipline**.

---

## 2. Kubernetes Deployment Architecture

The application is deployed using standard Kubernetes resources aligned with EKS best practices.

### 2.1 Deployment

A `Deployment` resource manages the application lifecycle.

Key characteristics:

- RollingUpdate strategy with zero downtime
    
- Replica count managed dynamically via HPA
    
- Stateless pod design enabling safe rescheduling
    
- Explicit resource requests and limits
    

The deployment is designed to tolerate:

- rolling upgrades
    
- pod restarts
    
- node terminations
    

This mirrors how frontend or API services are typically deployed in production clusters.

---

### 2.2 Service

A `ClusterIP` Service provides stable networking for the application.

Design considerations:

- decouples pod IPs from clients
    
- enables horizontal scaling without client awareness
    
- compatible with ingress or service mesh layers
    

---

### 2.3 Resource Requests and Limits

Each container defines CPU and memory requests and limits to ensure:

- predictable scheduling
    
- protection against noisy-neighbor issues
    
- reliable autoscaling signals
    

This configuration reflects common defaults in shared production clusters.

---

### 2.4 Liveness and Readiness Probes

Separate probes are configured to:

- gate traffic only to ready pods
    
- allow Kubernetes to self-heal unrecoverable failures
    

This separation prevents cascading failures during startup or transient load.

---

### 2.5 Horizontal Pod Autoscaler (HPA)

Autoscaling is configured using **CPU and memory utilization** via the autoscaling/v2 API.

This enables the service to:

- scale out under load
    
- scale in during low traffic
    
- maintain SLOs without manual intervention
    

---

### 2.6 PodDisruptionBudget (PDB)

A PodDisruptionBudget ensures minimum availability during:

- node upgrades
    
- cluster maintenance
    
- voluntary disruptions
    

This prevents full service outages during infrastructure operations.

---

## 3. Helm Chart 

In addition to raw manifests, the deployment is packaged as a **Helm chart**.

The Helm chart demonstrates:

- configuration-driven deployments
    
- environment portability
    
- reuse across teams and clusters
    

Templates cover Deployment, Service, HPA, and PDB without over-templating.

---

## 4. Observability Implementation

Observability is implemented across **metrics, logs, and traces**, aligned with the **golden signals** model.

---

### 4.1 Metrics & Dashboards

Metrics are exposed in Prometheus format and visualized using Grafana.

Dashboards focus on **user-impacting signals**:

- Latency (p50, p95, p99)
    
- Error rate (HTTP 5xx)
    
- Request volume (RPS)
    
- CPU and memory usage
    

Dashboards are:

- exportable as JSON
    
- environment-agnostic
    
- suitable for reuse across clusters
    

Low traffic volume in a local environment is expected; correctness of instrumentation and queries is the objective.

---

### 4.2 Logging Pipeline

Centralized logging is implemented using **Fluent Bit** as a DaemonSet.

Design characteristics:

- node-level log collection
    
- no application sidecars
    
- EKS-compatible operational model
    

This minimizes application overhead and aligns with production logging architectures.

---

### 4.3 Tracing (OpenTelemetry)

Distributed tracing is implemented using **OpenTelemetry Collector**.

Key properties:

- centralized trace ingestion
    
- vendor-neutral pipeline
    
- decoupling of instrumentation from backend choice
    

This mirrors real production tracing setups where exporters can evolve independently.

---

# Service Level Objectives (SLO)

## NGINX Sample Application

---

## 5. Purpose & Scope

This document defines the Service Level Objectives (SLOs) for the NGINX sample application deployed on Kubernetes in an EKS-like environment.

The goals are to:

- establish clear reliability expectations
    
- define measurable Service Level Indicators (SLIs)
    
- quantify acceptable failure using error budgets
    
- describe alerting strategies aligned with SRE best practices
    

This SLO is designed for a stateless, user-facing HTTP service and reflects how similar services are operated in production.

---

## 6. Service Overview

- **Service type:** Stateless HTTP application
    
- **Runtime:** Kubernetes (EKS-like)
    
- **Traffic pattern:** Client requests via Service
    
- **Scaling:** HPA (CPU + memory)
    
- **Availability protection:** PDB, rolling updates
    
- **Observability:** Metrics, logs, traces
    

---

## 7. User Journeys (What Matters)

From a user perspective, the service is healthy if:

- HTTP requests succeed
    
- responses are delivered within acceptable latency
    
- availability is maintained during deployments and node disruptions
    

SLOs are defined strictly around **user-visible behavior**, not internal implementation details.

---

## 8. Service Level Indicators (SLIs)

### 8.1 Availability SLI

**Definition:**  
Ratio of successful HTTP responses to total requests.

- Success: HTTP 2xx, 3xx
    
- Failure: HTTP 5xx
    

**Measurement source:**  
Prometheus HTTP request counters.

---

### 8.2 Latency SLI

**Definition:**  
Time taken to serve HTTP requests at the application boundary.

Evaluated at:

- p50
    
- p95
    
- p99
    

**Measurement source:**  
Histogram-based request duration metrics.

---

### 8.3 Error Rate SLI

**Definition:**  
Percentage of HTTP 5xx responses over total requests.

Captures:

- application failures
    
- resource exhaustion
    
- dependency-related issues
    

---

## 9. Service Level Objectives (SLOs)

### 9.1 Availability SLO

|Objective|Target|
|---|---|
|Availability|99.9%|

This allows controlled failure while maintaining user trust.

---

### 9.2 Latency SLO

|Percentile|Target|
|---|---|
|p95|< 200 ms|
|p99|< 500 ms|

Thresholds balance user experience with realistic production conditions.

---

### 9.3 Error Rate SLO

|Metric|Target|
|---|---|
|HTTP 5xx|< 0.1%|

---

## 10. Error Budget

### 10.1 Calculation

For a 99.9% availability SLO:

- Allowed error rate: 0.1%
    
- Error budget (30 days): ~43 minutes of unavailability
    

---

### 10.2 Usage Policy

- Error budget consumption is expected
    
- Budget exhaustion triggers:
    
    - deployment freeze
        
    - focus on reliability work
        
    - reduced feature velocity
        

This aligns with **blameless SRE practices**, not punitive enforcement.

---

## 11. Alerting Strategy

Alerts are designed to be:

- actionable
    
- low noise
    
- proportional to user impact
    

### Fast-Burn Alert

- Error rate > 5% for 5 minutes
    
- Immediate incident response
    

### Slow-Burn Alert

- Error rate > 0.1% for 1 hour
    
- Reliability work prioritized
    

### High Latency Alert

- p99 latency > 500 ms for 10 minutes
    
- Investigate saturation and scaling
    

### Traffic Anomaly Alert

- Sudden spike or drop in traffic
    
- Validate upstream behavior and autoscaling
    

---

## 12. Operational Response (Runbook Summary)

When alerts fire:

- inspect dashboards
    
- review pod health and restarts
    
- check recent deployments
    
- validate HPA and PDB behavior
    
- correlate logs and traces
    

This supports calm, structured incident handling.

---

## 13. Scaling & Resilience Considerations

- HPA absorbs load spikes
    
- resource limits prevent noisy neighbors
    
- PDB ensures availability during maintenance
    
- rolling updates minimize user impact
    

These mechanisms collectively support the defined SLOs.

---

## 14. Summary

This document defines the Service Level Objectives (SLOs) for the NGINX sample application running on Kubernetes in an EKS-like environment.

The SLOs focus on **user-visible reliability**, measured through availability, latency, and error rate SLIs derived from production-grade observability signals. Error budgets are used to quantify acceptable failure and guide operational and delivery decisions.

Alerting is designed to distinguish between **fast-burning incidents** and **gradual reliability degradation**, enabling timely and actionable responses without alert fatigue.

The Kubernetes configuration and observability stack are aligned to support these objectives, ensuring predictable behavior during scaling events, deployments, and infrastructure disruptions.

These SLOs are intended to evolve based on real operational data and error budget consumption.
