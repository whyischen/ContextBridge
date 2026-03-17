import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Terminal, ArrowRight, Copy, Check, BookOpen, Zap, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import usageEn from '../../../docs/usage_en.md?raw';
import usageZh from '../../../docs/usage_zh.md?raw';
import openclawEn from '../../../docs/openclaw_integration_en.md?raw';
import openclawZh from '../../../docs/openclaw_integration_zh.md?raw';

interface LandingPageProps {
  lang: 'en' | 'zh';
  t: any;
  copied: boolean;
  copyInstallCmd: () => void;
}

type DocType = 'guide' | 'openclaw' | null;

const DOC_MAP = {
  guide:    { en: usageEn,    zh: usageZh },
  openclaw: { en: openclawEn, zh: openclawZh },
} as const;

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 18 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5, delay, ease: 'easeOut' as const },
});

const fadeUpView = (delay = 0) => ({
  initial: { opacity: 0, y: 18 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.5, delay, ease: 'easeOut' as const },
});

export default function LandingPage({ lang, t, copied, copyInstallCmd }: LandingPageProps) {
  const [activeDoc, setActiveDoc] = useState<DocType>(null);
  const location = useLocation();

  useEffect(() => {
    if (location.hash === '#docs-center') {
      setTimeout(() => {
        document.getElementById('docs-center')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  }, [location.hash]);

  const handleDocClick = (id: 'guide' | 'openclaw') => {
    if (activeDoc === id) {
      setActiveDoc(null);
    } else {
      setActiveDoc(id);
      setTimeout(() => {
        document.getElementById('doc-content')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    }
  };

  const docCards = [
    { id: 'guide'    as const, icon: BookOpen, title: t.docCards[0].title, desc: t.docCards[0].desc },
    { id: 'openclaw' as const, icon: Zap,      title: t.docCards[1].title, desc: t.docCards[1].desc },
  ];

  return (
    <main className="min-h-screen">

      {/* Hero */}
      <section className="relative flex flex-col items-center text-center px-4 pt-28 sm:pt-36 pb-20 sm:pb-28 overflow-hidden">
        <div className="pointer-events-none absolute inset-0 -z-10">
          <div className="absolute left-1/2 top-0 -translate-x-1/2 w-[800px] h-[500px] bg-gradient-to-b from-indigo-500/10 via-violet-500/5 to-transparent rounded-full blur-3xl" />
        </div>

        <motion.h1
          {...fadeUp(0.08)}
          className="max-w-3xl text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight leading-[1.1] text-slate-900 dark:text-white mb-5"
        >
          {t.heroTitle}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-500">
            {t.heroHighlight}
          </span>
          {t.heroSuffix}
        </motion.h1>

        <motion.p
          {...fadeUp(0.16)}
          className="max-w-xl text-base sm:text-lg text-slate-500 dark:text-slate-400 leading-relaxed mb-10"
        >
          {t.subtitle}
        </motion.p>

        <motion.div {...fadeUp(0.24)} className="flex flex-col sm:flex-row items-center gap-3 w-full max-w-md">
          <div className="flex items-center justify-between w-full sm:flex-1 bg-white dark:bg-[#111] border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 font-mono text-sm shadow-sm">
            <span className="text-slate-500 dark:text-slate-400 select-all truncate">pip install cbridge-agent</span>
            <button
              onClick={copyInstallCmd}
              className="ml-3 flex-shrink-0 text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
              title="Copy"
            >
              {copied ? <Check size={15} className="text-emerald-500" /> : <Copy size={15} />}
            </button>
          </div>
          <a
            href="#quickstart"
            className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white text-sm font-medium transition-colors shadow-lg shadow-indigo-500/25 whitespace-nowrap w-full sm:w-auto"
          >
            {t.quickStart}
            <ArrowRight size={15} />
          </a>
        </motion.div>
      </section>

      {/* Features */}
      <section className="px-4 sm:px-6 pb-20 sm:pb-28">
        <div className="max-w-5xl mx-auto grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {t.features.map((feature: any, idx: number) => (
            <motion.div
              key={idx}
              {...fadeUpView(0.05 * idx)}
              className="group bg-white dark:bg-[#111] border border-slate-200 dark:border-white/[0.07] rounded-2xl p-6 hover:border-indigo-300 dark:hover:border-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/5 transition-all duration-300"
            >
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-50 to-violet-50 dark:from-indigo-500/10 dark:to-violet-500/10 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform duration-300">
                <feature.icon size={18} className="text-indigo-600 dark:text-indigo-400" />
              </div>
              <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-1.5">{feature.title}</h3>
              <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Docs */}
      <section id="docs-center" className="px-4 sm:px-6 pb-20 sm:pb-28">
        <div className="max-w-3xl mx-auto">
          <motion.h2 {...fadeUpView(0)} className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white mb-8 text-center">
            {t.docsSection}
          </motion.h2>

          <div className="grid sm:grid-cols-2 gap-4">
            {docCards.map(({ id, icon: Icon, title, desc }, idx) => {
              const isActive = activeDoc === id;
              return (
                <motion.button
                  key={id}
                  {...fadeUpView(0.08 * idx)}
                  onClick={() => handleDocClick(id)}
                  className={`group text-left rounded-2xl p-6 border transition-all duration-300 ${
                    isActive
                      ? 'bg-indigo-50 dark:bg-indigo-500/10 border-indigo-300 dark:border-indigo-500/40'
                      : 'bg-white dark:bg-[#111] border-slate-200 dark:border-white/[0.07] hover:border-indigo-300 dark:hover:border-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/5'
                  }`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-300 ${
                      isActive
                        ? 'bg-indigo-100 dark:bg-indigo-500/20'
                        : 'bg-gradient-to-br from-indigo-50 to-violet-50 dark:from-indigo-500/10 dark:to-violet-500/10 group-hover:scale-105'
                    }`}>
                      <Icon size={18} className="text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <ChevronDown size={15} className={`mt-1 transition-all duration-300 ${
                      isActive ? 'rotate-180 text-indigo-500 dark:text-indigo-400' : 'text-slate-300 dark:text-slate-600 group-hover:text-indigo-400'
                    }`} />
                  </div>
                  <h4 className={`text-sm font-semibold mb-1.5 ${isActive ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-900 dark:text-white'}`}>
                    {title}
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
                </motion.button>
              );
            })}
          </div>

          <AnimatePresence>
            {activeDoc && (
              <motion.div
                id="doc-content"
                key={activeDoc}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
                className="overflow-hidden"
              >
                <div className="mt-4 bg-white dark:bg-[#111] border border-slate-200 dark:border-white/[0.07] rounded-2xl px-6 sm:px-10 py-8">
                  <div className="prose prose-slate dark:prose-invert max-w-none
                    prose-headings:font-semibold prose-headings:tracking-tight
                    prose-h1:text-xl prose-h1:mb-5 prose-h1:pb-4 prose-h1:border-b prose-h1:border-slate-200 dark:prose-h1:border-white/10
                    prose-h2:text-lg prose-h2:mt-8 prose-h2:mb-3
                    prose-h3:text-base prose-h3:mt-6 prose-h3:mb-2
                    prose-p:text-slate-600 dark:prose-p:text-slate-400 prose-p:leading-7 prose-p:text-sm
                    prose-li:text-slate-600 dark:prose-li:text-slate-400 prose-li:text-sm
                    prose-a:text-indigo-600 dark:prose-a:text-indigo-400 prose-a:no-underline hover:prose-a:underline
                    prose-strong:text-slate-800 dark:prose-strong:text-slate-200
                    prose-code:text-indigo-600 dark:prose-code:text-indigo-400 prose-code:bg-indigo-50 dark:prose-code:bg-indigo-500/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-md prose-code:text-[0.8em] prose-code:font-normal prose-code:before:content-none prose-code:after:content-none
                    prose-pre:bg-slate-50 dark:prose-pre:bg-[#0f0f0f] prose-pre:border prose-pre:border-slate-200 dark:prose-pre:border-white/[0.07] prose-pre:rounded-xl prose-pre:text-xs
                  ">
                    <ReactMarkdown rehypePlugins={[rehypeRaw]}>
                      {DOC_MAP[activeDoc][lang]}
                    </ReactMarkdown>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </section>

      {/* Quick Start */}
      <section id="quickstart" className="px-4 sm:px-6 pb-24 sm:pb-32">
        <div className="max-w-2xl mx-auto">
          <motion.h2 {...fadeUpView(0)} className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white mb-8 text-center">
            {t.quickStart}
          </motion.h2>
          <motion.div
            {...fadeUpView(0.08)}
            className="rounded-2xl overflow-hidden border border-slate-200 dark:border-white/[0.07] shadow-xl shadow-black/5 dark:shadow-black/30"
          >
            <div className="flex items-center gap-2 px-4 py-3 bg-slate-100 dark:bg-[#161616] border-b border-slate-200 dark:border-white/[0.07]">
              <span className="w-3 h-3 rounded-full bg-red-400/80" />
              <span className="w-3 h-3 rounded-full bg-amber-400/80" />
              <span className="w-3 h-3 rounded-full bg-emerald-400/80" />
              <div className="flex items-center gap-1.5 ml-3">
                <Terminal size={12} className="text-slate-400 dark:text-slate-500" />
                <span className="text-xs font-mono text-slate-400 dark:text-slate-500">bash</span>
              </div>
            </div>
            <div className="bg-white dark:bg-[#0f0f0f] px-5 py-5 font-mono text-xs sm:text-sm space-y-4">
              {t.steps.map((step: any, idx: number) => (
                <div key={idx}>
                  <p className="text-slate-400 dark:text-slate-500 mb-1 select-none">{step.comment}</p>
                  <p className="text-indigo-600 dark:text-indigo-300">
                    <span className="text-slate-400 dark:text-slate-500 mr-2 select-none">$</span>
                    {step.cmd}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

    </main>
  );
}
