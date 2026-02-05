# SRE_task
Monitoring Demo: Python Metrics App + Prometheus + Grafana
=========================================================

Overview
--------
This repository contains everything required to build, deploy, and monitor a custom Python metrics application in Kubernetes using Prometheus and Grafana.

Features:
- Custom Python app exposing metrics (/metrics) using prometheus_client.
- Dockerfile builds a non-root minimal image.
- Kubernetes manifests to deploy app, Prometheus, node-exporter, and Grafana.
- Prometheus scrapes the app and node metrics.
- Grafana dashboard visualizing app and node metrics.
- Example alert rule for high request latency.

Repository layout
-----------------
- app/
  - Dockerfile
  - requirements.txt
  - metrics_app.py
- k8s/
  - namespace.yaml
  - app-deployment.yaml
  - app-service.yaml
  - prometheus-configmap.yaml
  - prometheus-deployment.yaml
  - prometheus-service.yaml
  - prometheus-alerts-configmap.yaml
  - node-exporter-daemonset.yaml
  - grafana-dashboards-configmap.yaml
  - grafana-deployment.yaml
  - grafana-dashboard.json
- README.md

Docker image build
------------------
1. Build:
   docker build -t abhilash483/sretask/metrics-app:latest ./app

2. Push:
   docker push abhilash483/sretask/metrics-app:latest

   Or, for kind:
   kind load docker-image abhilash483/sretask/metrics-app:latest

Security and best practices
---------------------------
- Non-root: the Dockerfile creates a non-root user and runs the app as that user.
- Minimal base: python:3.11-slim is used to keep image size small.
- Small dependency set pinned in requirements.txt.

Metrics exposed by the application
----------------------------------
- example_app_requests_total{path}: Counter of total requests handled, labeled by path.
  - Useful for request rate, traffic distribution, SLA baselining.
- example_app_requests_inprogress: Gauge counting in-flight requests.
  - Useful to detect backpressure (high concurrent requests).
- example_app_process_seconds_bucket: Histogram of request processing durations.
  - Enables p50/p95/p99 latency calculations via histogram_quantile.

Why these metrics?
- Counters + rates (via Prometheus rate()) show traffic trends.
- In-progress gauge helps detect concurrency spikes or saturation.
- Histogram allows percentile latency analysis that most summaries cannot provide.

Prometheus config notes
-----------------------
- Scrape targets: metrics-app (app service) and node-exporter (node metrics).
- Scrape interval is 15s (configurable).
- Alerts: example rule "HighRequestLatency" triggers if p95 > 1s for 2 minutes.

Grafana dashboard
-----------------
- The provided dashboard (Grafana provisioning) has panels:
  - Request rate by path (per-second rates).
  - In-progress requests (current gauge).
  - p95 request processing time (histogram_quantile).
  - Node CPU usage (1 - idle) per instance.

- To produce the screenshot deliverable:
  - Visit Grafana UI (http://localhost:3000 if port-forwarded).
  - Open Dashboard "Metrics App + Node Overview".
  - Use Grafana Share -> Export -> PNG or take a screenshot.

Alerts and observability decisions
---------------------------------
- Alert on high p95 latency rather than average latency to catch tail latency spikes.
- A 2-minute "for" duration prevents flapping due to short-lived blips.
- Severity label is included for routing in real systems.

How to run locally (minikube/kind)
----------------------------------
1. Build the image and make it available to the cluster (push to registry or load into kind).
2. Apply manifests (see earlier section commands).
3. Port-forward Grafana & Prometheus:
   kubectl -n monitoring-demo port-forward svc/grafana 3000:3000
   kubectl -n monitoring-demo port-forward svc/prometheus 9090:9090
4. Generate traffic to /work and verify metrics in Prometheus and graphs in Grafana.

Extending this setup
--------------------
- Use the Prometheus Operator (kube-prometheus-stack) for production-grade deployment (ServiceMonitors, PrometheusRules).
- Secure Grafana with authentication and setup datasources via secrets.
- Persist Prometheus and Grafana storage (PVCs) instead of emptyDir.
- Add node exporter service discovery using Kubernetes service endpoints or use kubelet metrics.

Deliverables checklist
----------------------
- Dockerfile: app/Dockerfile
- Monitoring manifests: everything under k8s/
- Grafana dashboard: k8s/grafana-dashboards-configmap.yaml (example-dashboard.json) and k8s/grafana-dashboard.json
- README: this file explaining choices and steps

Contact / Questions
-------------------
If you need help adapting the manifests to your specific cluster (EKS/GKE/AKS/minikube/kind), tell me which environment you use and I will provide an adapted set of commands (e.g., service type LoadBalancer, ingress, or kind load commands).