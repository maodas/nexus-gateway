"use client";

import React, { useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line, Doughnut } from "react-chartjs-2";
import { Activity, PieChart } from "lucide-react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface ChartsSectionProps {
  departmentData: Record<
    string,
    {
      cached?: number;
      live?: number;
      tokens?: number;
      request_count?: number;
      requests_count?: number;
      tokens_total?: number;
      tokens_processed?: number;
      cost_total_usd?: number;
      cost_usd?: number;
      cost_saved_usd?: number;
    }
  >;
}

export const ChartsSection: React.FC<ChartsSectionProps> = ({ departmentData }) => {
  const [metricMode, setMetricMode] = useState<"requests" | "cached" | "tokens">("requests");

  // Latency Comparison Data (Line Chart)
  const lineChartData = {
    labels: ["t-6", "t-5", "t-4", "t-3", "t-2", "t-1", "NOW"],
    datasets: [
      {
        label: "Semantic Cache (ms)",
        data: [2.5, 2.2, 2.8, 2.1, 2.4, 2.0, 2.5],
        borderColor: "#3b82f6", // Blue-500
        backgroundColor: "rgba(59, 130, 246, 0.05)",
        fill: true,
        tension: 0.2,
      },
      {
        label: "Groq LLaMA-3.3 (ms)",
        data: [142, 138, 155, 129, 148, 135, 140],
        borderColor: "#10b981", // Emerald-500
        backgroundColor: "transparent",
        fill: false,
        tension: 0.2,
      },
      {
        label: "OpenRouter Fallback (ms)",
        data: [850, 920, 780, 890, 910, 840, 870],
        borderColor: "#f59e0b", // Amber-500
        backgroundColor: "transparent",
        borderDash: [4, 4],
        fill: false,
        tension: 0.2,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#09090b",
        titleColor: "#f4f4f5",
        bodyColor: "#a1a1aa",
        borderColor: "#27272a",
        borderWidth: 1,
        padding: 8,
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(39, 39, 42, 0.6)" },
        ticks: { color: "#71717a", font: { size: 10, family: "monospace" } },
      },
      y: {
        grid: { color: "rgba(39, 39, 42, 0.6)" },
        ticks: { color: "#71717a", font: { size: 10, family: "monospace" } },
        title: { display: true, text: "Latency (ms)", color: "#71717a", font: { size: 10, family: "monospace" } },
      },
    },
  };

  // Department Dataset selection mapped directly to request_count / tokens_total
  const deptKeys = Object.keys(departmentData);
  const deptLabels = deptKeys.length
    ? deptKeys.map((k) => k.toUpperCase())
    : ["GENERAL", "ENGINEERING", "MARKETING"];

  const getMetricValues = () => {
    if (!deptKeys.length) return [0, 0, 0];
    return Object.values(departmentData).map((v) => {
      if (metricMode === "cached") {
        return v.cached ?? 0;
      } else if (metricMode === "tokens") {
        return v.tokens ?? v.tokens_processed ?? v.tokens_total ?? 0;
      } else {
        return v.requests_count ?? v.request_count ?? 0;
      }
    });
  };

  const doughnutData = {
    labels: deptLabels,
    datasets: [
      {
        label: metricMode === "cached" ? "Cached Hits" : metricMode === "tokens" ? "Tokens Consumed" : "Requests Processed",
        data: getMetricValues(),
        backgroundColor: [
          "#3b82f6", // Blue
          "#10b981", // Emerald
          "#f59e0b", // Amber
          "#8b5cf6", // Purple
          "#ec4899", // Pink
        ],
        borderColor: "#18181b",
        borderWidth: 2,
      },
    ],
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom" as const,
        labels: {
          color: "#a1a1aa",
          font: { size: 10, family: "monospace" },
          usePointStyle: true,
          padding: 12,
        },
      },
      tooltip: {
        backgroundColor: "#09090b",
        titleColor: "#f4f4f5",
        bodyColor: "#a1a1aa",
        borderColor: "#27272a",
        borderWidth: 1,
        callbacks: {
          label: (context: any) => ` ${context.label}: ${context.raw} ${metricMode.toUpperCase()}`,
        },
      },
    },
    cutout: "65%",
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
      {/* Latency Comparison Line Chart */}
      <div className="lg:col-span-2 dev-card p-4 flex flex-col justify-between">
        <div className="flex items-center justify-between gap-2 mb-3 pb-2 border-b border-zinc-800">
          <div className="flex items-center gap-2 font-mono">
            <Activity className="w-4 h-4 text-blue-400" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-200">
              Latency Benchmarks &amp; Provider Speedup
            </h3>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-950 text-blue-400 border border-zinc-800">
            PROBE: ACTIVE
          </span>
        </div>

        {/* Custom HTML Flexbox Legend */}
        <div className="flex items-center justify-center gap-6 text-xs text-zinc-400 font-mono mb-3 flex-wrap">
          <span className="flex items-center">
            <span className="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2" />
            Semantic Cache (ms)
          </span>
          <span className="flex items-center">
            <span className="inline-block w-3 h-3 rounded-full bg-emerald-500 mr-2" />
            Groq LLaMA-3.3 (ms)
          </span>
          <span className="flex items-center">
            <span className="inline-block w-3 h-3 rounded-full bg-amber-500 mr-2" />
            OpenRouter Fallback (ms)
          </span>
        </div>

        <div className="h-56 sm:h-64 w-full">
          <Line data={lineChartData} options={lineOptions} />
        </div>
      </div>

      {/* Department Telemetry Doughnut Chart */}
      <div className="dev-card p-4 flex flex-col justify-between">
        <div className="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-zinc-800 font-mono">
          <div className="flex items-center gap-2">
            <PieChart className="w-4 h-4 text-emerald-400" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-200">
              Department Telemetry
            </h3>
          </div>

          <div className="flex items-center gap-1 bg-zinc-950 p-0.5 rounded border border-zinc-800 text-[10px]">
            <button
              onClick={() => setMetricMode("requests")}
              className={`px-1.5 py-0.5 rounded transition-colors cursor-pointer ${
                metricMode === "requests" ? "bg-zinc-800 text-zinc-100 font-bold" : "text-zinc-500 hover:text-zinc-300"
              }`}
              title="Total Requests"
            >
              Reqs
            </button>
            <button
              onClick={() => setMetricMode("cached")}
              className={`px-1.5 py-0.5 rounded transition-colors cursor-pointer ${
                metricMode === "cached" ? "bg-blue-950 text-blue-400 font-bold" : "text-zinc-500 hover:text-zinc-300"
              }`}
              title="Cached Hits"
            >
              Cache
            </button>
            <button
              onClick={() => setMetricMode("tokens")}
              className={`px-1.5 py-0.5 rounded transition-colors cursor-pointer ${
                metricMode === "tokens" ? "bg-emerald-950 text-emerald-400 font-bold" : "text-zinc-500 hover:text-zinc-300"
              }`}
              title="Token Consumption"
            >
              Tokens
            </button>
          </div>
        </div>

        <div className="h-56 sm:h-64 w-full flex items-center justify-center relative">
          <Doughnut data={doughnutData} options={doughnutOptions} />
        </div>
      </div>
    </div>
  );
};
