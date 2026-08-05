"use client";

import React from "react";
import { MessageSquare, ExternalLink, ShieldCheck } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="mt-12 border-t border-zinc-800 bg-zinc-950/80 py-4 px-6 font-mono text-xs text-zinc-400">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Left / Main Text Attribution */}
        <div className="flex items-center gap-1.5 flex-wrap text-center sm:text-left">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
          <span>Created, designed, developed &amp; deployed by</span>
          <a
            href="https://maodas.online"
            target="_blank"
            rel="noopener noreferrer"
            className="text-zinc-200 font-semibold hover:text-emerald-400 hover:underline transition-all inline-flex items-center gap-0.5"
          >
            <span>Marcos Rodas</span>
            <ExternalLink className="w-2.5 h-2.5 text-zinc-500" />
          </a>
        </div>

        {/* Right / WhatsApp Action Button */}
        <div className="flex items-center gap-3">
          <a
            href="https://wa.me/50240154866"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20 hover:border-emerald-500/50 transition-all font-mono text-xs group cursor-pointer"
            title="Contact Developer via WhatsApp"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <MessageSquare className="w-3.5 h-3.5 group-hover:scale-110 transition-transform" />
            <span>Contact Developer</span>
          </a>
        </div>
      </div>
    </footer>
  );
};
