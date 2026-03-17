import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import { BookOpen, Zap, ChevronDown } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import usageEn from '../../../docs/usage_en.md?raw';
import usageZh from '../../../docs/usage_zh.md?raw';
import openclawEn from '../../../docs/openclaw_integration_en.md?raw';
import openclawZh from '../../../docs/openclaw_integration_zh.md?raw';

type DocType = 'guide' | 'openclaw';

interface DocsPageProps {
  lang: 'en' | 'zh';
}

interface SidebarItem {
  id: DocType;
  labelEn: string;
  labelZh: string;
  icon: LucideIcon;
}

const sidebarItems: SidebarItem[] = [
  { id: 'guide',    labelEn: 'User Guide',          labelZh: '使用指南',      icon: BookOpen },
  { id: 'openclaw', labelEn: 'OpenClaw Integration', labelZh: 'OpenClaw 集成', icon: Zap },
];

const DOC_MAP = {
  guide:    { en: usageEn,    zh: usageZh },
  openclaw: { en: openclawEn, zh: openclawZh },
} as const;

const VALID: DocType[] = ['guide', 'openclaw'];

// ── Sidebar nav list ──────────────────────────────────────────────────────────
function NavList({ lang, activeDoc, onSelect }: { lang: 'en' | 'zh'; activeDoc: DocType; onSelect: (id: DocType) => void }) {
  return (
    <ul className="space-y-0.5">
      {sidebarItems.map((item) => {
        const Icon = item.icon;
        const active = activeDoc === item.id;
        return (
          <li key={item.id}>
            <button
              onClick={() => onSelect(item.id)}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors text-left ${
                active
                  ? 'bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-medium'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/[0.05] hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <Icon size={15} className="shrink-0" />
              {lang === 'en' ? item.labelEn : item.labelZh}
            </button>
          </li>
        );
      })}
    </ul>
  );
}

// ── DocsPage ──────────────────────────────────────────────────────────────────
export default function DocsPage({ lang }: DocsPageProps) {
  const { docType } = useParams<{ docType: string }>();
  const initial: DocType = VALID.includes(docType as DocType) ? (docType as DocType) : 'guide';
  const [activeDoc, setActiveDoc] = useState<DocType>(initial);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleSelect = (id: DocType) => {
    setActiveDoc(id);
    setMobileOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [activeDoc]);

  const activeItem = sidebarItems.find((i) => i.id === activeDoc)!;
  const ActiveIcon = activeItem.icon;
  const activeLabel = lang === 'en' ? activeItem.labelEn : activeItem.labelZh;
  const content = DOC_MAP[activeDoc][lang];

  return (
    <div className="min-h-screen bg-white dark:bg-[#1c1e21] pt-14">
      <div className="max-w-6xl mx-auto flex">

        {/* ── Desktop sidebar ─────────────────────────────────────────── */}
        <aside className="hidden lg:flex flex-col w-56 shrink-0 border-r border-slate-100 dark:border-white/[0.06]">
          <div className="sticky top-14 h-[calc(100vh-3.5rem)] overflow-y-auto px-3 py-6">
            <p className="px-3 mb-2 text-[11px] font-semibold uppercase tracking-widest text-slate-400 dark:text-slate-500">
              {lang === 'en' ? 'Docs' : '文档'}
            </p>
            <NavList lang={lang} activeDoc={activeDoc} onSelect={handleSelect} />
          </div>
        </aside>

        {/* ── Main content ────────────────────────────────────────────── */}
        <div className="flex-1 min-w-0">

          {/* Mobile nav bar */}
          <div className="lg:hidden sticky top-14 z-30 bg-white/90 dark:bg-[#1c1e21]/90 backdrop-blur border-b border-slate-100 dark:border-white/[0.06] px-4 py-2.5">
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="flex items-center gap-2 w-full text-sm font-medium text-slate-700 dark:text-slate-200"
            >
              <ActiveIcon size={15} className="text-indigo-500 shrink-0" />
              <span className="flex-1 text-left">{activeLabel}</span>
              <ChevronDown size={15} className={`transition-transform duration-200 ${mobileOpen ? 'rotate-180' : ''}`} />
            </button>
            {mobileOpen && (
              <div className="mt-2 pb-1">
                <NavList lang={lang} activeDoc={activeDoc} onSelect={handleSelect} />
              </div>
            )}
          </div>

          {/* Markdown content */}
          <article className="px-6 sm:px-10 py-10 max-w-3xl">
            <div className="prose prose-slate dark:prose-invert max-w-none
              prose-headings:font-semibold prose-headings:tracking-tight
              prose-h1:text-2xl prose-h1:mb-6 prose-h1:pb-4 prose-h1:border-b prose-h1:border-slate-200 dark:prose-h1:border-white/10
              prose-h2:text-xl prose-h2:mt-10 prose-h2:mb-4
              prose-h3:text-base prose-h3:mt-7 prose-h3:mb-3
              prose-p:text-slate-600 dark:prose-p:text-slate-400 prose-p:leading-7
              prose-li:text-slate-600 dark:prose-li:text-slate-400
              prose-a:text-indigo-600 dark:prose-a:text-indigo-400 prose-a:no-underline hover:prose-a:underline
              prose-strong:text-slate-800 dark:prose-strong:text-slate-200
              prose-code:text-indigo-600 dark:prose-code:text-indigo-400 prose-code:bg-indigo-50 dark:prose-code:bg-indigo-500/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-md prose-code:text-[0.8em] prose-code:font-normal prose-code:before:content-none prose-code:after:content-none
              prose-pre:bg-[#f8f9fc] dark:prose-pre:bg-[#1e2124] prose-pre:border prose-pre:border-slate-200 dark:prose-pre:border-white/[0.07] prose-pre:rounded-xl prose-pre:text-xs sm:prose-pre:text-sm
              prose-blockquote:border-indigo-300 dark:prose-blockquote:border-indigo-500/40 prose-blockquote:text-slate-500 dark:prose-blockquote:text-slate-400
            ">
              <ReactMarkdown rehypePlugins={[rehypeRaw]}>{content}</ReactMarkdown>
            </div>
          </article>
        </div>
      </div>
    </div>
  );
}
