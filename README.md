# Cloud Computing Mini Lab

Learn the core ideas behind cloud computing by running a bite-sized, but fully functional, distributed workload. This repository shows how containers, stateless services, message queues, and background workers collaborate the way they would in a real cloud deployment.

---

## What You Will Learn

- **Virtualized compute:** All app components run inside containers to mimic how cloud providers package workloads.
- **Managed data services:** Redis stands in for a managed cache/queue service (think AWS ElastiCache or Azure Cache for Redis).
- **Asynchronous processing:** The API publishes jobs, while the worker scales independently to handle long-running work.
- **Infrastructure as code mindset:** A single `docker-compose.yml` file describes the entire deployment, similar to Terraform or CloudFormation stacks.
- **Observability hooks:** Health checks and verbose logging mirror how production services advertise their status.

---

## High-Level Architecture

```
           +-------------+        enqueue job        +--------------+
Client --> |  API (Node) | ------------------------> |   Redis MQ    |
           +-------------+ <------- job status ------ +--------------+
                     |                                  ^
                     |                                  |
                     v         pull & process           |
               +------------+ --------------------------+
               | Worker PY  |
               +------------+
```

- `services/api`: Node.js REST API that accepts text workloads, stores status metadata, and pushes jobs to Redis.
- `services/worker`: Python worker that consumes queued jobs, simulates CPU work, and streams results back to Redis.
- `redis`: Acts as both the queue and a lightweight metadata store.

Run one worker for a warm-up lab or several to simulate horizontal scaling.

---

## Quick Start (Docker)

1. **Prerequisites:** Docker Desktop 4.x (or any Docker + Compose v2 installation).
2. Copy environment defaults and tweak as needed:
   ```powershell
   Copy-Item env.sample .env
   ```
3. Build and launch the stack:
   ```powershell
   docker compose up --build
   ```
4. Open http://localhost:8080/health to confirm the API is live.
5. Submit a job:
   ```powershell
   Invoke-RestMethod -Uri http://localhost:8080/jobs -Method Post -Body (@{ text = 'Cloud computing rocks!' } | ConvertTo-Json) -ContentType 'application/json'
   ```
6. Poll the job status:
   ```powershell
   Invoke-RestMethod -Uri http://localhost:8080/jobs/<JOB_ID> -Method Get
   ```

Stop everything with `docker compose down`.

---

## Running Without Docker

1. **Redis:** Install locally or run `docker run -p 6379:6379 redis:7`.
2. **API service:**
   ```powershell
   cd services/api
   npm install
   npm run dev
   ```
3. **Worker service:**
   ```powershell
   cd services/worker
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python worker.py
   ```

Each component reads the same environment variables defined in `env.sample`.

---

## REST API Cheat Sheet

| Method | Path          | Description                              |
| ------ | ------------- | ---------------------------------------- |
| GET    | `/health`     | Liveness probe used by load balancers.   |
| POST   | `/jobs`       | Submit text payloads for asynchronous processing. |
| GET    | `/jobs/:id`   | Inspect the status/result of a job.      |
| GET    | `/jobs`       | (Optional) List the most recent jobs.    |

**Payload example**

```json
{
  "text": "Explain cloud computing in one sentence."
}
```

**Response example**

```json
{
  "jobId": "0d7bf72f-21bf-4baa-9136-1b09fcdd34de",
  "status": "queued"
}
```

---

## Learning Guide

Additional background notes live in `docs/cloud-basics.md` and walk through:

1. IaaS vs. PaaS vs. FaaS.
2. Why containers make portability trivial.
3. Strategies for scaling stateless services.
4. Observability must-haves.

Use this repository as a starting point, then port the same stack to Kubernetes, ECS, or serverless functions to keep exploring.

---

## Next Steps

- Swap Redis with a managed queue (SQS, Pub/Sub) to compare operational trade-offs.
- Add authentication + rate limiting to simulate multi-tenant SaaS needs.
- Extend the worker so that heavy CPU jobs rely on spot instances or serverless function bursts.

Happy cloud hacking! ☁️


