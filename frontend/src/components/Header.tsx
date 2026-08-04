"use client";

import React from "react";
import { RefreshCw, Terminal, HelpCircle } from "lucide-react";

interface HeaderProps {
  onRefresh: () => void;
  isRefreshing: boolean;
  lastUpdated: string;
  onOpenSystemInfo: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  onRefresh,
  isRefreshing,
  lastUpdated,
  onOpenSystemInfo,
}) => {
  return (
    <header className="border-b border-zinc-800 bg-zinc-900/90 px-6 py-3.5 mb-6 sticky top-0 z-40 backdrop-blur-md">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Brand & System Status */}
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded-md bg-zinc-950 border border-zinc-800 text-zinc-100">
            <Terminal className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-bold text-zinc-100 tracking-tight">
                NexusGateway
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-950 text-zinc-400 border border-zinc-800">
                v1.0.0-prod
              </span>
            </div>
            <p className="text-xs text-zinc-400 font-mono">
              LLM Cost Autopilot &amp; Semantic Proxy Telemetry
            </p>
          </div>
        </div>

        {/* Live Status Indicators & Controls */}
        <div className="flex items-center gap-3 text-xs font-mono">
          <div className="flex items-center gap-2 px-3 py-1 rounded bg-zinc-950 border border-zinc-800 text-zinc-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-zinc-400">STATUS:</span>
            <span className="text-emerald-400 font-bold">OPERATIONAL</span>
          </div>

          {/* System Info Button */}
          <button
            onClick={onOpenSystemInfo}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-zinc-950 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 transition-colors cursor-pointer"
            title="Open System Architecture Overview"
          >
            <HelpCircle className="w-3.5 h-3.5 text-blue-400" />
            <span>System Info</span>
          </button>

          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="flex items-center gap-2 px-3 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 transition-colors disabled:opacity-50 cursor-pointer"
            title="Refresh Telemetry"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-emerald-400" : ""}`} />
            <span>SYNC</span>
          </button>
        </div>
      </div>
    </header>
  );
};
