# Student REST API

A Student CRUD REST API built using **Python**, **Flask**, **SQLAlchemy**, and **PostgreSQL**, containerized using **Docker** and orchestrated using **Docker Compose** as part of the **One2N SRE Bootcamp**.

The project demonstrates REST API development, database migrations, containerization, Docker Compose, Gunicorn, Makefile automation, logging, testing, and environment variable configuration.
---

## Features

- Create Student
- Get All Students
- Get Student by ID
- Update Student
- Delete Student
- API Versioning (`/api/v1`)
- Health Check Endpoint
- Logging
- Input Validation
- Error Handling
- Database Migrations using Flask-Migrate
- PostgreSQL Database
- Docker Multi-stage Build
- Docker Compose
- Gunicorn Production Server
- Makefile Automation
- Unit Testing using Pytest
---

## Project Structure

```
student-rest-api/
│
├── app/
├── migrations/
├── tests/
├── instance/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── run.py
├── README.md
├── .env
└── .env.example
```

---

## Tech Stack

- Python 3.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Alembic
- Gunicorn
- Docker
- Docker Compose
- GNU Make
- Pytest

---

## Prerequisites

- Docker
- Docker Compose
- GNU Make
- Git

---


## Docker Setup

Build the Docker image

```bash
make build
```

Start the complete development environment

```bash
make up
```

This command automatically:

1. Starts PostgreSQL
2. Waits for PostgreSQL to become ready
3. Builds the REST API image
4. Runs database migrations
5. Starts the API

Check running containers

```bash
make ps
```

View logs

```bash
make logs
```

Stop all services

```bash
make down
```

Clean containers, images and volumes

```bash
make clean
----------
## Database Migration

Database migrations are automatically executed when running:

```bash
make up
```

To execute manually:

```bash
docker compose exec api flask db upgrade
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /healthcheck | Health Check |
| POST | /api/v1/students | Create Student |
| GET | /api/v1/students | Get All Students |
| GET | /api/v1/students/{id} | Get Student |
| PUT | /api/v1/students/{id} | Update Student |
| DELETE | /api/v1/students/{id} | Delete Student |

---

## Run the Application

```bash
make up
```

API

```
http://localhost:5000
```

Health Check

```
http://localhost:5000/healthcheck
```
## Running Tests

Run all tests

```bash
## Running Tests

Using local Python:

```bash
python -m pytest -v
```

Or inside Docker:

```bash
docker compose exec api pytest -v

```

---

## Environment Variables

The application uses the following environment variables:

```text
DATABASE_URL=postgresql+psycopg2://<db-user>:<db-password>@db:5432/studentdb
PORT=5000
DEBUG=False
SECRET_KEY=your-secret-key
```
------------

## Postman Collection

Import the Postman collection from the `postman/` folder.

---

## Future Improvements

- GitHub Actions CI/CD Pipeline
- Kubernetes Deployment
- Prometheus Monitoring
- Grafana Dashboards
- Helm Charts
- ArgoCD Deployment
- Terraform Infrastructure Automation

## Make Targets

| Command | Description |
|----------|-------------|
| `make build` | Build Docker image |
| `make up` | Start PostgreSQL, run migrations and start API |
| `make ps` | Show running containers |
| `make logs` | View application logs |
| `make down` | Stop all containers |
| `make clean` | Remove containers, volumes and images |

---


# Milestone 7 – Deploy REST API on Kubernetes

## Objective

Deploy the Student REST API and PostgreSQL on a Kubernetes cluster using Minikube while following production-style deployment practices.

## Components

- Namespace
- ConfigMap
- Deployment
- Service
- PostgreSQL
- Init Container
- HashiCorp Vault
- External Secrets Operator
- SecretStore
- ExternalSecret

## Kubernetes Architecture

```text
API Pods (2)
      │
      ▼
NodePort Service
      │
      ▼
PostgreSQL Service
      │
      ▼
PostgreSQL Pod

Vault
   │
External Secrets Operator
   │
Kubernetes Secret
```

## Resources Created

| Resource | Purpose |
|----------|---------|
| Namespace | Isolate project resources |
| ConfigMap | Store non-sensitive configuration |
| Deployment | Manage API Pods |
| Service | Expose API |
| PostgreSQL Deployment | Database |
| ClusterIP Service | Internal DB access |
| Vault | Store secrets |
| SecretStore | Connect ESO to Vault |
| ExternalSecret | Sync secrets |
| Kubernetes Secret | Used by API and DB |

## Verification Commands

```bash
kubectl get deployments -n student-api

kubectl get pods -n student-api

kubectl get svc -n student-api

kubectl get secretstore -n student-api

kubectl get externalsecret -n student-api
```

## Outcome

- API deployed with 2 replicas
- PostgreSQL deployed
- Database migrations executed using Init Container
- Secrets stored in Vault
- Secrets synchronized using External Secrets Operator
- API and Database consume Kubernetes Secrets

### Install HashiCorp Vault

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

kubectl create namespace vault

helm install vault hashicorp/vault \
  --namespace vault \
  --set "server.dev.enabled=true"
```

> Vault dev mode is used only for this bootcamp environment and should not be used in production.

### Install External Secrets Operator

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

kubectl create namespace external-secrets

helm install external-secrets \
  external-secrets/external-secrets \
  --namespace external-secrets
```

### Secret Flow

```text
HashiCorp Vault
      ↓
SecretStore
      ↓
ExternalSecret
      ↓
Kubernetes Secret
      ↓
API + PostgreSQL


# Milestone 8 - Deploy Using Helm Charts

## Objective

Convert the Kubernetes manifests from Milestone 7 into reusable Helm charts and deploy the Student REST API stack using Helm.

## Why Helm?

Raw Kubernetes manifests work well, but configuration becomes difficult to maintain across multiple environments.

Helm provides:

- Reusable Kubernetes templates
- Centralized configuration using `values.yaml`
- Application release management
- Upgrades and rollbacks
- Chart versioning
- Repeatable deployments

## Helm Chart Structure

```text
helm/
└── student-api/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── configmap.yaml
        ├── deployment.yaml
        ├── service.yaml
        ├── database.yaml
        └── external-secret.yaml
```

## Architecture

```text
                     Helm Release
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
      ConfigMap      API Deployment    PostgreSQL
                       2 Pods             Pod
                         |                 |
                         v                 v
                  NodePort Service   ClusterIP Service

Vault
  |
  v
SecretStore
  |
  v
ExternalSecret
  |
  v
Kubernetes Secret
  |
  +------> API
  |
  +------> PostgreSQL
```

## Validate the Helm Chart

```bash
helm lint ./helm/student-api
```

Render Kubernetes manifests without installing:

```bash
helm template student-api ./helm/student-api
```

## Install the Application

```bash
helm install student-api ./helm/student-api \
  -n student-api
```

## Upgrade or Install

```bash
helm upgrade --install student-api ./helm/student-api \
  -n student-api
```

This command installs the release if it does not exist and upgrades it if it already exists.

## Check Helm Releases

```bash
helm list -n student-api
```

## Check Release History

```bash
helm history student-api -n student-api
```

## Verify Kubernetes Resources

```bash
kubectl get pods -n student-api -o wide
kubectl get svc -n student-api
kubectl get externalsecret -n student-api
kubectl get secretstore -n student-api
```

## Verify API

```bash
curl http://$(minikube ip):<NODE_PORT>/healthcheck
```

Expected result:

```json
{
  "message": "Student API is running",
  "status": "UP"
}
```

## Helm Release Management

Upgrade:

```bash
helm upgrade student-api ./helm/student-api \
  -n student-api
```

View history:

```bash
helm history student-api -n student-api
```

Rollback:

```bash
helm rollback student-api <REVISION> \
  -n student-api
```

Uninstall:

```bash
helm uninstall student-api \
  -n student-api
```

## Outcome

- Converted raw Kubernetes manifests into reusable Helm templates.
- Centralized application configuration in `values.yaml`.
- Deployed two API replicas through Helm.
- Deployed PostgreSQL through Helm.
- Maintained application and database node placement.
- Integrated Vault with External Secrets Operator.
- Removed hardcoded database credentials from deployment configuration.
- Validated the chart using `helm lint` and `helm template`.
- Managed the application as a versioned Helm release.```

# Milestone 9 - One-Click Deployments with Argo CD

## Objective

Implement GitOps-based continuous deployment using Argo CD so that Kubernetes deployments are automatically synchronized from the Helm chart stored in Git.

## Why Argo CD?

GitHub Actions handles CI:

- Build application
- Run tests
- Run linting
- Build Docker image
- Push image to Docker Hub
- Update Helm `values.yaml`

Argo CD handles CD / GitOps:

- Watches Git for changes
- Uses Helm charts as the source of truth
- Compares desired state with the live Kubernetes cluster
- Automatically synchronizes changes
- Detects and repairs configuration drift
- Prunes resources removed from Git

## GitOps Architecture

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Build
    +--> Test
    +--> Lint
    +--> Docker Build
    +--> Docker Push
    +--> Update Helm image tag
    +--> Commit values.yaml
              |
              v
         Git Repository
              |
              v
           Argo CD
              |
          Auto Sync
              |
              v
          Helm Chart
              |
              v
        Kubernetes Cluster
```

## Argo CD Deployment

Argo CD components are deployed in the `argocd` namespace and scheduled on the node labeled:

```text
type=dependent_services
```

Verify:

```bash
kubectl get pods -n argocd -o wide
```

## Argo CD Application

The Student API is configured declaratively using:

```text
argocd/apps/student-api.yaml
```

Argo CD uses:

```text
Repository: https://github.com/Rc-Commit210/student-rest-api.git
Branch: master
Helm Path: helm/student-api
Namespace: student-api
```

## Automated Sync

The Argo CD Application uses:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

### Self-Healing

If the live Kubernetes configuration is manually changed and no longer matches Git, Argo CD automatically restores the Git-defined state.

Example test:

```bash
kubectl scale deployment student-api \
  -n student-api \
  --replicas=3
```

Since Git defines two replicas, Argo CD automatically restores:

```text
replicas = 2
```

### Pruning

If a Git-managed resource is removed from the Helm chart, Argo CD automatically removes that resource from Kubernetes.

This confirms that Git is the source of truth for the application deployment.

## GitHub Actions GitOps Flow

The CI workflow creates a Docker image tag using the Git commit SHA.

Example:

```text
a901309
```

Docker image:

```text
rcsanket753/student-rest-api:a901309
```

GitHub Actions then updates:

```yaml
image:
  repository: rcsanket753/student-rest-api
  tag: a901309
```

inside:

```text
helm/student-api/values.yaml
```

The workflow commits this change back to Git.

Argo CD detects the new Git revision and automatically deploys the new image.

## Verify Argo CD Application

```bash
kubectl get application student-api -n argocd
```

Expected:

```text
SYNC STATUS    Synced
HEALTH STATUS  Healthy
```

Check the Git revision synchronized by Argo CD:

```bash
kubectl get application student-api \
  -n argocd \
  -o jsonpath='{.status.sync.revision}{"\n"}'
```

## Verify Running Image

```bash
kubectl get deployment student-api \
  -n student-api \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

Example:

```text
rcsanket753/student-rest-api:a901309
```

## Useful Argo CD Commands

Check applications:

```bash
kubectl get applications -n argocd
```

Describe application:

```bash
kubectl describe application student-api -n argocd
```

Force refresh:

```bash
kubectl annotate application student-api \
  -n argocd \
  argocd.argoproj.io/refresh=hard \
  --overwrite
```

Check Argo CD Pods:

```bash
kubectl get pods -n argocd -o wide
```

## Outcome

- Argo CD deployed successfully in Kubernetes
- Argo CD scheduled on the `dependent_services` node
- Helm chart used as the deployment source of truth
- Argo CD Application created declaratively
- Automatic synchronization enabled
- Self-healing verified
- Pruning verified
- GitHub Actions updates Helm image tags automatically
- Docker images use Git commit SHA tags
- Argo CD automatically deploys new application versions
- Full CI + GitOps deployment workflow completed

## Author

**Sanket Chikhale**

Developed as part of the One2N SRE Bootcamp to demonstrate REST API development, containerization, database migrations, Docker Compose orchestration, and DevOps automation.
