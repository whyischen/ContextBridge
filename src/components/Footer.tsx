import React from 'react';
import { Github } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-100 dark:border-white/[0.06] py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400 dark:text-slate-500">
        <p>© {new Date().getFullYear()} ContextBridge — MIT License</p>
        <a
          href="https://github.com/whyischen/ContextBridge"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
        >
          <Github size={13} />
          GitHub
        </a>
      </div>
    </footer>
  );
}
