# Kubernetes + Observability + SLO

**Problem Statement: Deploy a Sample App with Production-Grade Standards**

---

## 1. Overview

This repository demonstrates how a **simple stateless application** can be deployed and operated on Kubernetes using **production-grade standards** for:

- workload configuration
    
- resilience and scaling
    
- observability (metrics, logs, traces)
    
- Service Level Objectives (SLOs)
    

The implementation mirrors patterns commonly used in **EKS-based environments**, focusing on **operability, reliability, and clarity**.

The deployed workload is a publicly available **NGINX container**, used intentionally as a neutral sample application to keep the focus on platform and reliability concerns.

---

## 2. Problem Statement

Deploy a sample containerized application on Kubernetes with:

### Kubernetes Requirements

- Deployment
    
- Service
    
- Horizontal Pod Autoscaler (CPU + memory)
    
- PodDisruptionBudget
    
- Liveness and readiness probes
    
- Resource requests and limits
    

### Observability Requirements

- Metrics dashboard covering golden signals:
    
    - latency (p50 / p95 / p99)
        
    - errors
        
    - request volume
        
    - CPU and memory usage
        
- Centralized log pipeline
    
- Distributed tracing example
    

### SLO Requirements

- Clear SLO definition (e.g., 99.9% availability)
    
- SLIs for latency and error rate
    
- Error budget calculation
    
- Alerting strategy:
    
    - fast burn
        
    - slow burn
        
    - high latency (p99)
        
    - traffic anomalies
        

---

## 3. Architecture Summary

The solution is structured to resemble an **EKS-like setup**, even when executed locally:

- Stateless application deployed via Kubernetes primitives
    
- Autoscaling driven by CPU and memory signals
    
- Availability protected through disruption budgets and rolling updates
    
- Observability implemented as cluster-level services, not app-embedded tooling
    

This separation ensures that **application logic remains simple**, while **platform capabilities handle reliability and visibility**.

---

## 4. Kubernetes Implementation

### Workload Configuration

The application is deployed using a standard Kubernetes `Deployment` with:

- rolling update strategy
    
- explicit resource requests and limits
    
- HTTP-based liveness and readiness probes
    

A `Service` exposes the workload internally.

### Scaling & Resilience

- **Horizontal Pod Autoscaler** scales on both CPU and memory utilization
    
- **PodDisruptionBudget** guarantees minimum availability during:
    
    - node maintenance
        
    - rescheduling events
        
    - rolling updates
        

These controls ensure predictable behavior under load and during infrastructure changes.

### EKS Compatibility

All manifests use upstream Kubernetes APIs and patterns compatible with managed Kubernetes platforms such as Amazon EKS.

---

## 5. Observability Design

### Metrics

Application and infrastructure metrics are collected and visualized using **Grafana**, following the **Golden Signals** model:

- **Latency**: p50, p95, p99 request duration
    
- **Errors**: HTTP 5xx rate
    
- **Traffic**: request volume (RPS)
    
- **Resources**: CPU and memory usage per workload
    

Dashboards are provided as JSON exports and validated via screenshots.

### Logging

A **Fluent Bit DaemonSet** is deployed for centralized log collection:

- node-level collection (no per-pod sidecars)
    
- scalable, low-overhead design
    
- compatible with common backends (CloudWatch, Elasticsearch, Datadog)
    

This reflects common production logging architectures.

### Tracing

Distributed tracing is enabled using **OpenTelemetry Collector**:

- OTLP receivers configured
    
- traces ingested and logged/exported for inspection
    
- demonstrates end-to-end request visibility
    

Tracing is intentionally lightweight and illustrative, aligned with platform-level instrumentation.

---

## 6. Helm Chart (Bonus)

In addition to raw Kubernetes manifests, the workload is packaged as a **Helm chart**:

- parameterized values for replicas, resources, and autoscaling
    
- reusable templates for deployment, service, HPA, and PDB
    
- supports environment-specific customization
    

The Helm chart demonstrates how the same workload can be promoted across environments with minimal changes.

---

## 7. Service Level Objectives (SLOs)

A dedicated SLO document defines:

- **Availability SLO** (e.g., 99.9%)
    
- **Latency SLIs** (p95 / p99 thresholds)
    
- **Error rate SLI** (HTTP 5xx)
    
- **Error budget** calculation and usage policy
    

Alerting strategies are designed to distinguish between:

- fast-burn incidents requiring immediate action
    
- slow-burn issues consuming error budget over time
    
- high-latency degradation
    
- traffic anomalies
    

The SLOs are intentionally **user-focused**, measuring only what impacts external consumers.

---

## 8. Operational Considerations

The configuration supports common operational workflows:

- safe scaling under load
    
- minimal disruption during deployments
    
- clear signals for debugging and incident response
    
- correlation across metrics, logs, and traces
    

The system is designed to be **observable first**, enabling effective on-call response without deep application knowledge

## 9. Deliverables Included

- Kubernetes manifests (Deployment, Service, HPA, PDB)
    
- Helm chart 
    
- Grafana dashboard JSON and screenshots
    
- Fluent Bit logging configuration
    
- OpenTelemetry Collector configuration
    
- SLO document 

## 10. Summary

This assignment demonstrates how a simple, stateless application can be deployed and operated on Kubernetes using **production-grade reliability, scalability, and observability practices**.

The solution intentionally focuses on:

- Correct Kubernetes primitives (Deployment, Service, HPA, PDB)
    
- Safe scaling and disruption handling
    
- Clear, user-centric observability signals
    
- Explicit Service Level Objectives with measurable SLIs
    
- Practical alerting aligned with error budgets
    

The design prioritizes **predictable behavior under load and failure**, clear operational visibility, and alignment with patterns commonly used in **EKS-based production environments**.

The included Kubernetes manifests, Helm chart, dashboards, logging pipeline, tracing setup, and SLO documentation together form a cohesive example of how platform and SRE teams evaluate readiness for real-world operation.

The outcome reflects an emphasis on **reliability, operability, and ownership**, which are core expectations for production systems.

