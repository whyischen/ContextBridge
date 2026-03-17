import React, { useRef, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { BookMarked, Github, Languages, Sun, Moon, Monitor, Blocks } from 'lucide-react';

interface NavbarProps {
  lang: 'en' | 'zh';
  setLang: (lang: 'en' | 'zh') => void;
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  isThemeOpen: boolean;
  setIsThemeOpen: (open: boolean) => void;
}

export default function Navbar({ lang, setLang, theme, setTheme, isThemeOpen, setIsThemeOpen }: NavbarProps) {
  const themeRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Close theme panel when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (themeRef.current && !themeRef.current.contains(e.target as Node)) {
        setIsThemeOpen(false);
      }
    }
    if (isThemeOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isThemeOpen, setIsThemeOpen]);

  const handleDocsClick = () => {
    if (location.pathname === '/') {
      document.getElementById('docs-center')?.scrollIntoView({ behavior: 'smooth' });
    } else {
      navigate('/#docs-center');
    }
  };

  const themeIcon = theme === 'light' ? <Sun size={15} /> : theme === 'dark' ? <Moon size={15} /> : <Monitor size={15} />;

  return (
    <nav className="fixed top-0 w-full border-b border-slate-200/80 dark:border-white/[0.06] bg-white/75 dark:bg-[#0a0a0a]/80 backdrop-blur-xl z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">

        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 font-semibold text-base group select-none">
          <div className="relative w-7 h-7 flex items-center justify-center">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-lg blur-sm opacity-40 group-hover:opacity-70 transition-opacity duration-300" />
            <div className="relative w-full h-full bg-gradient-to-br from-indigo-500 to-violet-600 rounded-lg flex items-center justify-center">
              <Blocks size={15} className="text-white" />
            </div>
          </div>
          <span className="text-slate-800 dark:text-white tracking-tight">ContextBridge</span>
        </Link>

        {/* Right controls */}
        <div className="flex items-center gap-1">

          {/* Docs */}
          <button
            onClick={handleDocsClick}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/[0.06] transition-colors"
          >
            <BookMarked size={15} />
            <span className="hidden sm:inline">Docs</span>
          </button>

          {/* GitHub */}
          <a
            href="https://github.com/whyischen/ContextBridge"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/[0.06] transition-colors"
          >
            <Github size={15} />
            <span className="hidden sm:inline">GitHub</span>
          </a>

          {/* Divider */}
          <div className="w-px h-4 bg-slate-200 dark:bg-white/10 mx-1" />

          {/* Language toggle */}
          <button
            onClick={() => setLang(lang === 'en' ? 'zh' : 'en')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/[0.06] transition-colors"
          >
            <Languages size={15} />
            <span className="text-xs font-medium">{lang === 'en' ? '中文' : 'EN'}</span>
          </button>

          {/* Theme toggle — after language */}
          <div ref={themeRef} className="relative">
            <button
              onClick={() => setIsThemeOpen(!isThemeOpen)}
              className="flex items-center justify-center w-8 h-8 rounded-md text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-white/[0.06] transition-colors"
              title="Toggle theme"
            >
              {themeIcon}
            </button>

            {isThemeOpen && (
              <div className="absolute right-0 top-full mt-1.5 w-36 bg-white dark:bg-[#1a1a1a] border border-slate-200 dark:border-white/10 rounded-xl shadow-xl shadow-black/10 dark:shadow-black/40 overflow-hidden py-1 z-50">
                {([
                  { value: 'light', label: lang === 'en' ? 'Light' : '浅色', icon: <Sun size={14} /> },
                  { value: 'dark',  label: lang === 'en' ? 'Dark'  : '深色', icon: <Moon size={14} /> },
                  { value: 'system',label: lang === 'en' ? 'System': '跟随系统', icon: <Monitor size={14} /> },
                ] as const).map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => { setTheme(opt.value); setIsThemeOpen(false); }}
                    className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm transition-colors ${
                      theme === opt.value
                        ? 'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-500/10'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-white/[0.04] hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    {opt.icon}
                    {opt.label}
                    {theme === opt.value && (
                      <span className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-500 dark:bg-indigo-400" />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
