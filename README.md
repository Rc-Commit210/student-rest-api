# Student REST API — SRE Bootcamp Project

A production-style Student REST API used to learn and implement software engineering, containerization, CI/CD, Kubernetes, GitOps, secrets management, observability, logging, dashboards, and alerting.

## Architecture

Client
  |
  v
Student REST API (Flask/Gunicorn)
  |
  v
PostgreSQL

Platform:
- Docker
- Kubernetes / Minikube
- Helm
- Argo CD
- HashiCorp Vault
- External Secrets Operator

Observability:
- Prometheus
- Grafana
- Node Exporter
- kube-state-metrics
- PostgreSQL Exporter
- Blackbox Exporter
- Loki
- Promtail
- Slack Alerting

---

## Bootcamp Milestones

| Milestone | Description | Status |
|---|---|---|
| 1 | Build REST API | Complete |
| 2 | Containerize Application | Complete |
| 3 | One-Click Local Development | Complete |
| 4 | CI Pipeline | Complete |
| 5 | Bare Metal Deployment | Skipped |
| 6 | Kubernetes Cluster | Complete |
| 7 | Deploy Application to Kubernetes | Complete |
| 8 | Helm Charts | Complete |
| 9 | Argo CD / GitOps | Complete |
| 10 | Observability Stack | Complete |
| 11 | Dashboards & Alerts | Complete |

---

## REST API

The Flask application provides:

- Health check
- Create student
- List students
- Get student
- Update student
- Delete student
- Input validation
- Duplicate-email handling
- Application logging
- Prometheus metrics

Example health endpoint:

```bash
curl http://localhost:5000/healthcheck
