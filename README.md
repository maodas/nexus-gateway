# NexusGateway ⚡

**NexusGateway** is an enterprise-grade LLM Cost Autopilot, Semantic Proxy, and Fallback Gateway designed to optimize AI infrastructure spend, provide sub-millisecond semantic caching, enforce tenant rate limits, and deliver zero-downtime multi-provider resilience.

---

## 🌟 Key Features

- **FinOps Cost Autopilot**: Dynamic model routing based on budget constraints, prompt token complexity, and price-per-token optimization (e.g., routing to Groq, OpenRouter, or fallback providers).
- **Semantic Caching Proxy**: Sub-millisecond response caching via Upstash Redis vector similarity search.
- **AI Resilience Engine**: Automated circuit breaking, exponential backoff retries, and seamless provider fallback chains.
- **Tenant Auth & Quotas**: Token-bucket rate limiting and API key verification for multi-tenant isolation.
- **Real-Time Analytics**: End-to-end latency metrics, token consumption tracking, and cost savings telemetry.

---

## 📁 Repository Layout

```text
nexus-gateway/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── gateway.py
│   │   │           ├── analytics.py
│   │   │           └── health.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── redis.py
│   │   ├── services/
│   │   │   ├── router_engine.py
│   │   │   ├── semantic_cache.py
│   │   │   ├── cost_tracker.py
│   │   │   └── resilience.py
│   │   └── schemas/
│   │       ├── gateway.py
│   │       └── analytics.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/             # Next.js Dashboard (Sprint 4)
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python**: 3.10+
- **Docker** (optional): For containerized deployment

### 1. Backend Environment Setup

Navigate to the backend directory and set up a Python virtual environment:

```bash
cd backend

# Create Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Environment Variables Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
PROJECT_NAME="NexusGateway"
VERSION="1.0.0"

# Redis Config (Upstash)
UPSTASH_REDIS_REST_URL="https://your-redis-instance.upstash.io"
UPSTASH_REDIS_REST_TOKEN="your-upstash-token"

# LLM Providers API Keys
GROQ_API_KEY="gsk_..."
OPENROUTER_API_KEY="sk-or-..."

# Security
GATEWAY_AUTH_KEY="nexus-secret-tenant-key"
```

### 3. Running the Server

Start the development server with Uvicorn:

```bash
# From backend/ directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 🐳 Docker Support

Build and run using Docker:

```bash
cd backend
docker build -t nexus-gateway-backend .
docker run -d -p 8000:8000 --env-file .env nexus-gateway-backend
```

---

## 📄 License

MIT License. Designed & Built for Enterprise AI Infrastructure.
