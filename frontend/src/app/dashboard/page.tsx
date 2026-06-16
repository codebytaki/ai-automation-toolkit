"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const modules = [
    { href: "/dashboard/agents", icon: "🤖", title: "AI Agents", desc: "Build and run autonomous AI agents", color: "from-purple-500/20 to-purple-600/5" },
    { href: "/dashboard/workflows", icon: "🔄", title: "Workflows", desc: "Automate with drag & drop builder", color: "from-blue-500/20 to-blue-600/5" },
    { href: "/dashboard/chat", icon: "💬", title: "Multi-AI Chat", desc: "Compare 6+ models simultaneously", color: "from-green-500/20 to-green-600/5" },
    { href: "/dashboard/files", icon: "📁", title: "File AI", desc: "Process PDFs, DOCX, CSV with AI", color: "from-yellow-500/20 to-yellow-600/5" },
    { href: "/dashboard/prompts", icon: "📚", title: "Prompt Library", desc: "Browse 200+ curated AI prompts", color: "from-red-500/20 to-red-600/5" },
    { href: "/dashboard/integrations", icon: "🔌", title: "Integrations", desc: "Connect GitHub, Slack, Notion & more", color: "from-cyan-500/20 to-cyan-600/5" },
];

const stats = [
    { label: "Agent Runs", value: "—", icon: "🤖" },
    { label: "Workflow Runs", value: "—", icon: "🔄" },
    { label: "Tokens Used", value: "—", icon: "🧠" },
    { label: "AI Cost (month)", value: "$0.00", icon: "💰" },
];

export default function DashboardPage() {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate loading stats — real implementation calls /api/v1/analytics/overview
        const timer = setTimeout(() => setLoading(false), 800);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100">
            {/* Top Nav */}
            <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <span className="text-2xl">⚡</span>
                    <span className="font-bold text-lg">AI Automation Toolkit</span>
                </div>
                <nav className="flex items-center gap-4 text-sm text-gray-400">
                    <Link href="/" className="hover:text-white transition-colors">Home</Link>
                    <a href="https://github.com/codebytaki/ai-automation-toolkit"
                        className="hover:text-white transition-colors">GitHub</a>
                    <Link href="/dashboard/settings"
                        className="px-4 py-1.5 border border-gray-700 rounded-lg hover:border-gray-500 transition-colors">
                        Settings
                    </Link>
                </nav>
            </header>

            <div className="max-w-6xl mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
                <p className="text-gray-400 mb-8">Your AI automation command center</p>

                {/* Stats Row */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    {stats.map((s) => (
                        <div key={s.label} className="glass rounded-xl p-4">
                            <div className="text-2xl mb-1">{s.icon}</div>
                            <div className="text-2xl font-bold">{loading ? <span className="animate-pulse">...</span> : s.value}</div>
                            <div className="text-sm text-gray-500">{s.label}</div>
                        </div>
                    ))}
                </div>

                {/* Module Grid */}
                <h2 className="text-xl font-semibold mb-4">Modules</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {modules.map((m) => (
                        <Link key={m.href} href={m.href}
                            className={`glass rounded-xl p-6 bg-gradient-to-br ${m.color} hover:scale-[1.01] transition-all duration-200 hover:border-white/20`}>
                            <div className="text-3xl mb-3">{m.icon}</div>
                            <h3 className="font-semibold text-lg mb-1">{m.title}</h3>
                            <p className="text-sm text-gray-400">{m.desc}</p>
                            <div className="mt-4 text-purple-400 text-sm font-medium">Open →</div>
                        </Link>
                    ))}
                </div>

                {/* Quick actions */}
                <div className="mt-8 p-6 glass rounded-xl">
                    <h2 className="text-lg font-semibold mb-4">Quick Start</h2>
                    <div className="flex flex-wrap gap-3">
                        {[
                            { href: "/dashboard/agents", label: "🤖 New Agent" },
                            { href: "/dashboard/workflows", label: "🔄 New Workflow" },
                            { href: "/dashboard/chat", label: "💬 Multi-AI Chat" },
                            { href: "/dashboard/files", label: "📁 Upload File" },
                        ].map((a) => (
                            <Link key={a.href} href={a.href}
                                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm transition-colors">
                                {a.label}
                            </Link>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
