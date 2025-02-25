// frontend/app/page.tsx
"use client";

import { useState } from "react";
import SearchBar from "@/components/search-bar";
import SearchResults from "@/components/search-results";
import AgentWorkflow from "@/components/agent-workflow";
import FinalAnalysis from "@/components/final-analysis";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/sonner";
import { Sparkles } from "lucide-react";

export default function Page() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = (query: string) => {
    setLoading(true);
    fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    })
      .then((res) => res.json())
      .then((resData) => {
        setData(resData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching analysis data:", err);
        setLoading(false);
      });
  };

  const handleClear = () => {
    setData(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-background/50 to-background transition-all duration-500">
      <div
        className={`transition-all duration-500 ${
          !data
            ? "flex flex-col items-center justify-center h-screen"
            : "container max-w-4xl mx-auto px-4 py-8"
        }`}
      >
        <div className={`${!data ? "text-center" : ""}`}>
          {!data && (
            <div className="flex flex-col items-center gap-2 mb-4">
              <Sparkles className="h-10 w-10 text-primary" />
              <h1 className="text-4xl font-extrabold bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 bg-clip-text text-transparent animate-fadeIn">
                CrewAI Analysis
              </h1>
            </div>
          )}
          <SearchBar onSearch={handleSearch} loading={loading} onClear={handleClear} />
          {!data && (
            <p className="mt-4 text-muted-foreground">
              Enter your query to start the analysis.
            </p>
          )}
        </div>
        {data && (
          <div className="space-y-4 mt-8">
            <SearchResults data={data} />
            <AgentWorkflow data={data} />
            <FinalAnalysis data={data} />
            {/* New Chat Button */}
            <div className="mt-8 flex justify-center">
              <Button variant="outline" onClick={handleClear} className="transition-all duration-300 hover:scale-105">
                New Chat
              </Button>
            </div>
          </div>
        )}
      </div>
      <Toaster />
    </main>
  );
}
