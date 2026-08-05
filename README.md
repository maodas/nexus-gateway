# ⚡ NexusGateway | Enterprise LLM FinOps & Resilience Proxy

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15+-000000?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![Upstash Redis](https://img.shields.io/badge/Upstash_Redis-Serverless-FF4400?style=for-the-badge&logo=redis)](https://upstash.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

NexusGateway is a high-performance, enterprise-grade LLM FinOps autopilot and resilience proxy. Designed to manage corporate AI budgets and guarantee zero-downtime inference, it provides real-time token arbitrage tracking, multi-tenant department budget governance, sub-millisecond semantic response caching, automated PII scrubbing, and automated circuit-breaker provider failovers.

---

## 🏛️ System Architecture

```text
                                  ┌────────────────────────┐
                                  │ Next.js Telemetry UI   │
                                  │ (FinOps Dashboard)     │
                                  └───────────┬────────────┘
                                              │ HTTP Requests
                                              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ NEXUSGATEWAY ROUTER ENGINE (FastAPI)                                                    │
│                                                                                        │
│  ┌────────────────────────┐    ┌────────────────────────┐    ┌──────────────────────┐  │
│  │ Layer 1/2 Guardrails   ├───►│ PII Regex Scrubber     ├───►│ Upstash Semantic     │  │
│  │ (Intent & Policy)      │    │ (Card/SSN/API Redact) │    │ Cache (SHA-256)      │  │
│  └────────────────────────┘    └────────────────────────┘    └──────────┬───────────┘  │
│                                                                         │              │
│                                           ┌─────────────────────────────┴────────────┐ │
│                                           │ Primary: Groq Llama-3.3-70b              │ │
│                                           └─────────────────────────────┬────────────┘ │
│                                                                         │ (503 / Fail) │
│                                           ┌─────────────────────────────▼────────────┐ │
│                                           │ Fallback: OpenRouter Resilience Route    │ │
│                                           └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Technical Capabilities

### 💰 FinOps Autopilot & Token Governance
- **Department Budget Isolation**: Tracks usage, token volume, and dollar spend across departments (`Engineering`, `Finance`, `Marketing`, `General`). Enforces budget caps to prevent runaway API costs.
- **Dynamic Arbitrage Calculation**: Measures prompt execution costs against standard industry benchmarks (GPT-4o baseline) to calculate dynamic dollars saved ($).

### ⚡ Sub-Millisecond Semantic Response Caching
- **Namespaced Upstash Redis Cache**: Fast lookup using prompt normalization and SHA-256 hashing.
- **Instant Speedup & Zero Token Cost**: Serves identical or semantically similar prompts in <2.5 ms with $0.00 LLM cost.

### 🛡️ Dual-Layer Enterprise Guardrails & Security
- **Layer 1 (Sub-1ms Regex Pre-Check)**: Fast deterministic filtering of prohibited categories (off-topic non-business prompts) with typo-tolerant matching.
- **Layer 2 (Semantic Intent Judge)**: Non-blocking small LLM evaluation (`llama-3.1-8b-instant`) to classify user intent against corporate compliance policies.
- **PII Data Scrubber**: Intercepts and masks sensitive credentials (Credit Cards, SSNs, Emails, API Keys) before sending requests to external providers.

### 🔄 Circuit Breaker Resilience & Chaos Engineering
- **Automated Failover**: Real-time circuit breaker tracking provider health states (`HEALTHY`, `OPEN`, `HALF_OPEN`).
- **Zero-Downtime Provider Arbitrage**: Seamlessly fails over from primary provider (Groq) to secondary provider (OpenRouter) during HTTP 500/503 outages or rate limits.
- **Chaos Testing Outage Simulator**: Integrated toggle switch to simulate primary provider outages and test resilience in real-time.

---

## 🛠️ Technology Stack

- **Backend Framework**: Python 3.11, FastAPI, Uvicorn (Async IO Event Loop)
- **HTTP Client**: `httpx.AsyncClient` (Non-blocking asynchronous calls)
- **Cache & Telemetry Database**: Upstash Redis (Serverless REST API)
- **LLM Providers**: Groq API (`llama-3.3-70b-versatile`), OpenRouter API (`openrouter/free`)
- **Frontend Dashboard**: Next.js 15, TypeScript, Tailwind CSS, Chart.js / Lucide Icons
- **DevOps & Cloud Pipeline**: Vercel (Frontend Edge) + Render (Backend Container)

---

## 🚀 Quickstart & Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/maodas/nexus-gateway.git
cd nexus-gateway
```

### 2. Backend Configuration
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file inside `backend/`:
```env
PROJECT_NAME="NexusGateway"
GROQ_API_KEY="gsk_your_groq_api_key"
OPENROUTER_API_KEY="sk-or-v1-your_openrouter_api_key"
UPSTASH_REDIS_REST_URL="https://your-upstash-redis.upstash.io"
UPSTASH_REDIS_REST_TOKEN="your_upstash_redis_token"
GATEWAY_AUTH_KEY="nexus-secret-auth-key"
```

Start Backend Server:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Dashboard Setup
```bash
cd ../frontend
npm install
```

Create `.env.local` inside `frontend/`:
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_GATEWAY_AUTH_KEY="nexus-secret-auth-key"
```

Start Development Server:
```bash
npm run dev -- -p 3002
```

---

## 📊 API Reference

### `POST /api/v1/gateway/chat/completions`

Send a completion request through the smart router engine.

#### Headers:
```http
Content-Type: application/json
X-Gateway-API-Key: nexus-secret-auth-key
X-Simulate-Outage: groq
```

#### Request Body:
```json
{
  "department": "engineering",
  "messages": [
    { "role": "user", "content": "What is the FinOps ROI of semantic caching?" }
  ],
  "temperature": 0.7
}
```

---

## 📄 License

Distributed under the MIT License. Developed by Marcos Rodas ([@maodas](https://github.com/maodas)).
