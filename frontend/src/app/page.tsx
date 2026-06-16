import Link from "next/link";

const features = [
    { icon: "🤖", title: "AI Agent Builder", desc: "Create autonomous AI agents with GPT-4, Claude, Gemini. Add tools, memory, and deploy." },
    { icon: "🔄", title: "Workflow Builder", desc: "Drag & drop automation like n8n + Zapier. Trigger → AI → API → Notify." },
    { icon: "🌐", title: "Browser Automation", desc: "AI controls Playwright browser. Click, fill forms, extract data automatically." },
    { icon: "💬", title: "Multi-AI Chat", desc: "Compare GPT-4, Claude, Gemini, Groq side-by-side. See cost and latency." },
    { icon: "📁", title: "File AI", desc: "Upload PDF, DOCX, CSV. AI summarize, analyze, translate, extract in seconds." },
    { icon: "📚", title: "Prompt Library", desc: "200+ curated prompts. Search, favorite, version control, share publicly." },
];

export default function HomePage() {
    return (
        <main className="min-h-screen flex flex-col">
            {/* Hero */}
            <section className="flex flex-col items-center justify-center text-center px-4 py-24 gap-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-purple-500/30 bg-purple-500/10 text-purple-300 text-sm mb-2">
                    <span>⚡</span> Open-source AI Automation Platform
                </div>

                <h1 className="text-5xl md:text-7xl font-bold tracking-tight max-w-4xl">
                    Automate <span className="gradient-text">Anything</span> with AI
                </h1>

                <p className="text-xl text-gray-400 max-w-2xl">
                    Agents · Workflows · Browser · Multi-AI Chat · File AI · 50+ Integrations — all in one modern platform.
                </p>

                <div className="flex gap-4 mt-4">
                    <Link href="/dashboard"
                        className="px-8 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition-colors">
                        Get Started Free →
                    </Link>
                    <a href="https://github.com/codebytaki/ai-automation-toolkit"
                        className="px-8 py-3 border border-gray-700 hover:border-gray-500 rounded-lg font-semibold transition-colors">
                        ⭐ Star on GitHub
                    </a>
                </div>

                {/* Stats */}
                <div className="flex gap-8 mt-8 text-center">
                    {[
                        { label: "AI Models", value: "10+" },
                        { label: "Integrations", value: "20+" },
                        { label: "Workflow Templates", value: "50+" },
                        { label: "Lines of Code", value: "12k+" },
                    ].map((s) => (
                        <div key={s.label}>
                            <div className="text-2xl font-bold text-purple-400">{s.value}</div>
                            <div className="text-sm text-gray-500">{s.label}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Features Grid */}
            <section className="px-4 py-16 max-w-6xl mx-auto w-full">
                <h2 className="text-3xl font-bold text-center mb-12">Everything you need to automate with AI</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {features.map((f) => (
                        <div key={f.title} className="glass rounded-xl p-6 hover:border-purple-500/30 transition-colors">
                            <div className="text-3xl mb-3">{f.icon}</div>
                            <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
                            <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA */}
            <section className="text-center py-20 px-4">
                <h2 className="text-3xl font-bold mb-4">Ready to automate?</h2>
                <p className="text-gray-400 mb-8">Open-source, self-hostable, MIT licensed.</p>
                <Link href="/dashboard"
                    className="px-10 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold text-lg hover:opacity-90 transition-opacity">
                    Open Dashboard →
                </Link>
            </section>

            {/* Footer */}
            <footer className="border-t border-gray-800 py-8 text-center text-gray-500 text-sm">
                <p>AI Automation Toolkit — Open-source · MIT License · Built by{" "}
                    <a href="https://github.com/codebytaki" className="text-purple-400 hover:underline">@codebytaki</a>
                </p>
            </footer>
        </main>
    );
}
