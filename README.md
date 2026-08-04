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
