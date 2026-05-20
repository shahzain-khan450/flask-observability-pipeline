# flask-observability-pipeline
# Multi-Service Flask Observability Pipeline 🚀

A production-grade local DevOps monitoring and observability stack. This project deploys a self-instrumented Python Flask application alongside a fully integrated Prometheus and Grafana telemetry pipeline using Docker container orchestration.

## 🏗️ Architecture Overview

- **Web Application:** Python Flask app instrumented via `prometheus_client`. Includes internal fault-injection logic (random latency spikes and HTTP 500 responses) to simulate realistic production traffic behavior.
- **Time-Series Database:** Prometheus configured to scrape application telemetry targets every 15 seconds.
- **Visualization Layer:** Grafana instance securely linked to the Prometheus data layer for real-time performance rendering.

## 🛠️ Technology Stack

- **Core:** Python 3 (Flask)
- **Containerization & Orchestration:** Docker, Docker Compose
- **Monitoring & Telemetry:** Prometheus (TSDB), PromQL
- **Data Visualization:** Grafana

---

## 📈 Monitoring Metric Formulas

The dashboard utilizes specialized PromQL queries to compute crucial performance KPIs:

### 1. Total Traffic Volume (Requests/Sec)
Tracks total incoming throughput trends normalized across a 1-minute rolling rate window:
```promql
sum(rate(app_requests_total[1m]))
