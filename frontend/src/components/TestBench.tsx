"use client";

import React, { useState } from "react";
import { Send, Terminal, Shield, AlertTriangle, CornerDownRight, AlertCircle, Sparkles } from "lucide-react";
import { sendGatewayCompletion, GatewayCompletionResponse } from "@/services/api";

interface TestBenchProps {
  onSuccess: (latencyMs?: number) => void;
}

export const TestBench: React.FC<TestBenchProps> = ({ onSuccess }) => {
  const [prompt, setPrompt] = useState(
    "What is the FinOps ROI for user test@company.com with card 4111-2222-3333-4444 and key gsk_1234567890abcdef1234567890?"
  );
  const [department, setDepartment] = useState("engineering");
  const [simulateOutage, setSimulateOutage] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GatewayCompletionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const samplePrompts = [
    {
      label: "PII Test",
      text: "Send report to admin@nexus.io with credit card 4532-1122-3344-5566 and SSN 123-45-6789.",
    },
    {
      label: "FinOps Prompt",
      text: "What is the FinOps ROI of semantic caching in enterprise LLM gateways?",
    },
    {
      label: "API Key Test",
      text: "Validate configuration for Groq key gsk_abcdef1234567890abcdef12345.",
    },
  ];

  const handleSend = async (customPrompt?: string) => {
    const textToSend = customPrompt || prompt;
    if (!textToSend.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await sendGatewayCompletion({
        messages: [{ role: "user", content: textToSend }],
        department: department,
        temperature: 0.7,
        max_tokens: 300,
        simulate_outage: simulateOutage ? "groq" : undefined,
      });

      setResult(res);
      onSuccess(res.latency_ms);
    } catch (err: any) {
      setError(err.message || "Failed to connect to Gateway API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dev-card p-5 border border-zinc-800 mb-6 font-mono">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-zinc-800">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <h2 className="text-xs font-bold text-zinc-100 uppercase tracking-wider">
            Live Gateway Test Bench &amp; Telemetry Log
          </h2>
        </div>

        {/* Controls: Chaos Toggle & Sample Prompts */}
        <div className="flex items-center gap-3 flex-wrap">
          {/* Chaos Test Toggle */}
          <label className="flex items-center gap-1.5 text-[10px] text-zinc-400 bg-zinc-950 px-2 py-1 rounded border border-zinc-800 cursor-pointer">
            <input
              type="checkbox"
              checked={simulateOutage}
              onChange={(e) => setSimulateOutage(e.target.checked)}
              className="rounded bg-zinc-900 border-zinc-700 text-amber-500 focus:ring-0 cursor-pointer"
            />
            <AlertTriangle className={`w-3.5 h-3.5 ${simulateOutage ? "text-amber-400 animate-pulse" : "text-zinc-600"}`} />
            <span className={simulateOutage ? "text-amber-400 font-bold" : ""}>
              SIMULATE GROQ OUTAGE
            </span>
          </label>

          {/* Quick Prompts */}
          <div className="flex items-center gap-1">
            <span className="text-[10px] text-zinc-500">PROMPTS:</span>
            {samplePrompts.map((p, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setPrompt(p.text);
                  handleSend(p.text);
                }}
                disabled={loading}
                className="text-[10px] px-2 py-0.5 rounded bg-zinc-950 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 transition-colors disabled:opacity-50 cursor-pointer"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Left Column: Prompt Input */}
        <div className="flex flex-col justify-between space-y-3">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-[11px] font-semibold text-zinc-400 uppercase">
                USER PROMPT INPUT
              </label>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-[10px] text-zinc-500">DEPT:</span>
                <select
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  className="text-xs bg-zinc-950 text-zinc-200 border border-zinc-800 rounded px-2 py-0.5 focus:outline-none focus:border-zinc-700"
                >
                  <option value="engineering">engineering</option>
                  <option value="marketing">marketing</option>
                  <option value="finance">finance</option>
                  <option value="general">general</option>
                </select>
              </div>
            </div>

            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              placeholder="Type request prompt containing PII or standard text..."
              className="w-full bg-zinc-950 text-zinc-200 text-xs p-3 rounded border border-zinc-800 focus:outline-none focus:border-zinc-700 font-mono resize-none"
            />
          </div>

          <div className="flex items-center justify-between pt-1">
            <span className="text-[10px] text-zinc-500">
              PII GUARDRAIL: AUTOMATIC SCRUBBING
            </span>
            <button
              onClick={() => handleSend()}
              disabled={loading || !prompt.trim()}
              className="px-4 py-1.5 rounded bg-zinc-100 hover:bg-white text-zinc-950 font-bold text-xs tracking-wide transition-all flex items-center gap-1.5 disabled:opacity-50 cursor-pointer"
            >
              {loading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-zinc-950/30 border-t-zinc-950 rounded-full animate-spin" />
                  <span>EXECUTING...</span>
                </>
              ) : (
                <>
                  <Send className="w-3.5 h-3.5" />
                  <span>EXECUTE REQUEST</span>
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="p-2.5 rounded bg-rose-950/40 border border-rose-900 text-rose-300 text-xs flex items-center gap-2 font-mono">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Right Column: Terminal JSON Telemetry Viewer */}
        <div className="terminal-container p-3.5 rounded border border-zinc-800 bg-zinc-950 text-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-zinc-900 text-[11px]">
              <span className="flex items-center gap-1 text-zinc-400">
                <CornerDownRight className="w-3.5 h-3.5 text-emerald-400" />
                TELEMETRY LOG STREAM
              </span>

              {result && (
                <div className="flex items-center gap-2">
                  {/* PII Redacted Pill Badge */}
                  {result.pii_redacted && (
                    <span className="px-2 py-0.5 rounded text-[10px] bg-purple-950 text-purple-300 border border-purple-800 font-bold flex items-center gap-1">
                      <Shield className="w-3 h-3 text-purple-400" />
                      PII SCRUBBER ACTIVE ({result.redacted_items_count} MASKED)
                    </span>
                  )}

                  {result.cached ? (
                    <span className="px-2 py-0.5 rounded text-[10px] bg-blue-950 text-blue-400 border border-blue-800 font-bold">
                      CACHE HIT [2.5ms]
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800 font-bold">
                      LLM PROXY [{result.provider_used}]
                    </span>
                  )}
                </div>
              )}
            </div>

            {result ? (
              <div className="space-y-2">
                {/* Outage Failover Alert Stream if OpenRouter fallback triggered during simulation */}
                {simulateOutage && result.provider_used === "openrouter" && (
                  <div className="p-2 rounded bg-amber-950/40 border border-amber-800 text-amber-300 text-[10px] font-mono flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                    <span>⚠️ Groq Circuit Breaker Triggered (503) &rarr; Fallback to OpenRouter (Success)</span>
                  </div>
                )}

                <div className="text-[11px] text-zinc-400 border-b border-zinc-900 pb-2 flex items-center justify-between">
                  <span>ID: <strong className="text-zinc-200">{result.id}</strong></span>
                  <span>Latency: <strong className="text-amber-400">{result.latency_ms} ms</strong></span>
                  <span>Cost: <strong className="text-emerald-400">${result.estimated_cost_usd.toFixed(6)}</strong></span>
                </div>

                <div className="text-zinc-300 text-[11px] leading-relaxed max-h-36 overflow-y-auto font-mono bg-zinc-900/50 p-2.5 rounded border border-zinc-900">
                  <span className="text-zinc-500">// Response Text:</span>
                  <p className="mt-1 text-zinc-200">{result.content}</p>
                </div>

                <div className="text-[10px] text-zinc-500 flex items-center justify-between pt-1">
                  <span>Tokens: {result.total_tokens} ({result.prompt_tokens} prompt / {result.completion_tokens} completion)</span>
                  <span>Model: {result.model_used}</span>
                </div>
              </div>
            ) : (
              <div className="h-36 flex flex-col items-center justify-center text-center text-zinc-600 font-mono text-xs">
                <Terminal className="w-6 h-6 mb-2 text-zinc-700" />
                <p>Ready. Execute a prompt with PII or simulated outage to inspect live telemetry.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
