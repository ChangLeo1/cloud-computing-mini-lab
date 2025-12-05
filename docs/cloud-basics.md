# Cloud Computing Crash Course

Use this project as your lab notebook while you explore the fundamentals below.

## 1. Cloud Service Models

| Model | You Manage | Provider Manages | Example |
| ----- | ---------- | ---------------- | ------- |
| IaaS  | OS, runtime, app code | Hardware, networking, virtualization | AWS EC2, Azure VM |
| PaaS  | App code, data | OS, runtime, scaling, patching | Heroku, Azure App Service |
| FaaS  | Function handler | Everything except your handler | AWS Lambda, Cloud Functions |

The `docker-compose.yml` file mimics IaaS: you control the runtime, while Docker simulates the provider’s hypervisor.

## 2. Why Containers Matter

- **Portability:** Container images run the same on a laptop or in a managed Kubernetes cluster.
- **Density:** Packing multiple services on a single VM leverages the provider’s billing model.
- **Isolation:** Namespaces keep workloads from interfering with each other, boosting reliability.

## 3. Stateless vs. Stateful

Stateless services (like the API here) can be scaled horizontally by simply adding replicas behind a load balancer. Stateful services (Redis) often use managed offerings in production to simplify replication, backups, and failovers.

## 4. Event-Driven & Asynchronous Work

The API and worker communicate through Redis queues:

1. The API enqueues a job and immediately returns a tracking ID.
2. Workers pull jobs as capacity allows, making the system naturally elastic.
3. Results are written back to Redis, so any API instance can respond to status requests.

This pattern is common in serverless pipelines, data processing backends, and ML batch jobs.

## 5. Observability

- `/health` endpoint shows how load balancers monitor service health.
- Structured logging (JSON-friendly) makes it easy to ship logs to CloudWatch, Stackdriver, or OpenTelemetry collectors.
- Redis contains near-real-time job metrics; exporting those to Prometheus would be a next step.

## 6. From Lab to Cloud

| Local Concept | Cloud Translation |
| ------------- | ----------------- |
| `docker-compose.yml` | Terraform/CloudFormation describing ECS, AKS, or GKE services |
| `redis` container | Managed cache (ElastiCache, Memorystore) |
| API container | Container workload on ECS Fargate / Cloud Run / App Service |
| Worker container | Batch jobs, serverless functions, or Kubernetes CronJobs |

Try re-deploying this stack to one of the services above, then measure latency, cost, and scaling behavior.



