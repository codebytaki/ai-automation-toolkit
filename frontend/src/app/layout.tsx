import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "react-hot-toast";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "AI Automation Toolkit",
    description: "Automate Anything with AI — Agents, Workflows, Browser, APIs, Files in one platform.",
    keywords: ["AI automation", "workflow builder", "AI agents", "LangGraph", "n8n alternative"],
    authors: [{ name: "codebytaki" }],
    openGraph: {
        title: "AI Automation Toolkit",
        description: "Open-source AI automation platform",
        type: "website",
    },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" className="dark">
            <body className={`${inter.className} bg-gray-950 text-gray-100 antialiased`}>
                {children}
                <Toaster
                    position="top-right"
                    toastOptions={{
                        style: { background: "#1f2937", color: "#f9fafb", border: "1px solid #374151" },
                    }}
                />
            </body>
        </html>
    );
}
