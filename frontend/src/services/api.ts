import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const GATEWAY_AUTH_KEY = process.env.NEXT_PUBLIC_GATEWAY_AUTH_KEY || "nexus-secret-auth-key-change-in-production";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
    "X-Nexus-Auth-Key": GATEWAY_AUTH_KEY,
    "X-Gateway-API-Key": GATEWAY_AUTH_KEY,
  },
  timeout: 30000, // Increased timeout to 30 seconds for safety
});

export interface AnalyticsSummary {
  total_requests: number;
  total_tokens: number;
  total_cost_usd: number;
  total_saved_usd?: number;
  cache_hits: number;
  cache_hit_rate_percentage: number;
  department_breakdown: Record<string, {
    cached?: number;
    live?: number;
    tokens?: number;
    requests_count?: number;
    request_count?: number;
    tokens_total?: number;
    tokens_processed?: number;
    cost_total_usd?: number;
    cost_usd?: number;
    cost_saved_usd?: number;
  }>;
}

export interface GatewayCompletionRequest {
  messages: Array<{ role: string; content: string }>;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  department?: string;
  simulate_outage?: string;
}

export interface GatewayCompletionResponse {
  id: string;
  provider_used: string;
  model_used: string;
  content: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  estimated_cost_usd: number;
  cached: boolean;
  latency_ms: number;
  pii_redacted?: boolean;
  redacted_items_count?: number;
  guardrail_triggered?: string;
}

export async function getAnalyticsSummary(): Promise<AnalyticsSummary> {
  try {
    const response = await apiClient.get<AnalyticsSummary>("/analytics/summary");
    return response.data;
  } catch (error) {
    console.warn("Backend telemetry offline or uninitialized:", error);
    return {
      total_requests: 0,
      total_tokens: 0,
      total_cost_usd: 0.0,
      total_saved_usd: 0.0,
      cache_hits: 0,
      cache_hit_rate_percentage: 0.0,
      department_breakdown: {},
    };
  }
}

export async function sendGatewayCompletion(
  payload: GatewayCompletionRequest
): Promise<GatewayCompletionResponse> {
  try {
    const headers: Record<string, string> = {
      "X-Nexus-Auth-Key": GATEWAY_AUTH_KEY,
      "X-Gateway-API-Key": GATEWAY_AUTH_KEY,
    };

    if (payload.simulate_outage) {
      headers["X-Simulate-Outage"] = payload.simulate_outage;
    }

    const response = await apiClient.post<GatewayCompletionResponse>("/gateway/chat/completions", payload, {
      headers,
    });
    return response.data;
  } catch (error: any) {
    const detail = error?.response?.data?.detail;
    if (detail && typeof detail === "object") {
      const errObj: any = new Error(detail.content || detail.detail || "Gateway Policy Blocked");
      errObj.guardrail_triggered = detail.guardrail_triggered || "Topic Policy (Off-Topic Intent)";
      errObj.content = detail.content || detail.detail || "🚫 PROMPT BLOCKED: Enterprise Policy restricts non-business topics on corporate channels.";
      throw errObj;
    }
    throw new Error(error?.response?.data?.detail || error.message || "Gateway API Error");
  }
}
