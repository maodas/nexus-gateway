"use client";

import React from "react";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  variant?: "emerald" | "blue" | "amber" | "zinc";
  badgeText?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  variant = "zinc",
  badgeText,
}) => {
  const variantStyles = {
    emerald: {
      accentText: "text-emerald-400",
      borderLeft: "border-l-2 border-l-emerald-500",
      badgeBg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    },
    blue: {
      accentText: "text-blue-400",
      borderLeft: "border-l-2 border-l-blue-500",
      badgeBg: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    },
    amber: {
      accentText: "text-amber-400",
      borderLeft: "border-l-2 border-l-amber-500",
      badgeBg: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    },
    zinc: {
      accentText: "text-zinc-100",
      borderLeft: "border-l-2 border-l-zinc-600",
      badgeBg: "bg-zinc-800 text-zinc-300 border-zinc-700",
    },
  };

  const style = variantStyles[variant];

  return (
    <div className={`dev-card dev-card-hover p-4 border border-zinc-800 ${style.borderLeft} flex flex-col justify-between`}>
      <div>
        <div className="flex items-center justify-between gap-2 mb-2">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-zinc-400 font-sans">
            {title}
          </span>
          <Icon className="w-4 h-4 text-zinc-500" />
        </div>

        <div className="flex items-baseline justify-between gap-2">
          <div className={`text-2xl font-bold font-mono tracking-tight ${style.accentText}`}>
            {value}
          </div>
          {badgeText && (
            <span className={`text-[10px] font-mono font-medium px-1.5 py-0.5 rounded border ${style.badgeBg}`}>
              {badgeText}
            </span>
          )}
        </div>
      </div>

      {subtitle && (
        <div className="mt-3 pt-2 border-t border-zinc-800/80 text-[11px] font-mono text-zinc-500">
          {subtitle}
        </div>
      )}
    </div>
  );
};
