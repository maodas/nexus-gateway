"use client";

import React from "react";
import { X, Zap, Shield, BarChart3, Terminal } from "lucide-react";

interface WelcomeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const WelcomeModal: React.FC<WelcomeModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-zinc-950/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="dev-card max-w-2xl w-full p-6 border border-zinc-800 bg-zinc-900 shadow-2xl relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-zinc-500 hover:text-zinc-300 p-1 rounded-md bg-zinc-950 border border-zinc-800 transition-colors cursor-pointer"
          title="Close Modal"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-lg bg-zinc-950 border border-zinc-800 text-emerald-400 font-mono">
            <Terminal className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-zinc-100 tracking-tight">
              Welcome to NexusGateway FinOps Telemetry
            </h2>
            <p className="text-xs text-zinc-400 font-mono">
              Enterprise LLM Cost Autopilot &amp; Resilience Gateway
            </p>
          </div>
        </div>

        {/* Core Highlights Grid Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-6">
          {/* Card 1: Semantic Caching */}
          <div className="p-4 rounded-lg bg-zinc-950 border border-zinc-800/80 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2 text-blue-400 font-mono text-xs font-bold">
                <Zap className="w-4 h-4 shrink-0" />
                <span>Semantic Cache</span>
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed font-sans">
                Sub-10ms response caching powered by Upstash Redis to reduce duplicate API costs to $0.00.
              </p>
            </div>
            <span className="mt-3 text-[10px] font-mono text-blue-400 font-semibold uppercase">
              NAMESPACED REDIS
            </span>
          </div>

          {/* Card 2: Circuit Breaker Failover */}
          <div className="p-4 rounded-lg bg-zinc-950 border border-zinc-800/80 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2 text-emerald-400 font-mono text-xs font-bold">
                <Shield className="w-4 h-4 shrink-0" />
                <span>Circuit Breaker</span>
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed font-sans">
                Zero-downtime provider fallback (Groq &rarr; OpenRouter) automatically handling HTTP errors &amp; 429 rate limits.
              </p>
            </div>
            <span className="mt-3 text-[10px] font-mono text-emerald-400 font-semibold uppercase">
              FAILOVER READY
            </span>
          </div>

          {/* Card 3: Multi-Tenant FinOps */}
          <div className="p-4 rounded-lg bg-zinc-950 border border-zinc-800/80 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2 text-amber-400 font-mono text-xs font-bold">
                <BarChart3 className="w-4 h-4 shrink-0" />
                <span>FinOps Autopilot</span>
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed font-sans">
                Real-time token accounting, cost savings tracking, and strict budget caps per department.
              </p>
            </div>
            <span className="mt-3 text-[10px] font-mono text-amber-400 font-semibold uppercase">
              GOVERNANCE ACTIVE
            </span>
          </div>
        </div>

        {/* Footer Action */}
        <div className="flex items-center justify-between pt-3 border-t border-zinc-800/80 font-mono">
          <span className="text-[10px] text-zinc-500">
            PRESS &lsquo;ESC&rsquo; OR BUTTON TO DISMISS
          </span>
          <button
            onClick={onClose}
            className="px-5 py-2 rounded bg-zinc-100 hover:bg-white text-zinc-950 font-bold text-xs tracking-wide transition-all cursor-pointer"
          >
            Explore Live Gateway &rarr;
          </button>
        </div>
      </div>
    </div>
  );
};
