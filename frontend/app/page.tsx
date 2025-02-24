// frontend/app/page.tsx
"use client";

import { useState } from "react";
import SearchBar from "@/components/search-bar";
import SearchResults from "@/components/search-results";
import AgentWorkflow from "@/components/agent-workflow";
import FinalAnalysis from "@/components/final-analysis";
import { Toaster } from "@/components/ui/sonner";

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
    <main className="min-h-screen bg-gradient-to-b from-background/50 to-background">
      <div className="container max-w-3xl mx-auto px-4 py-8 space-y-4">
        <div className="sticky top-4 z-10 mb-8">
          <SearchBar onSearch={handleSearch} loading={loading} onClear={handleClear} />
        </div>
        {data ? (
          <div className="space-y-4 transition-opacity duration-300">
            <SearchResults data={data} />
            <AgentWorkflow data={data} />
            <FinalAnalysis data={data} />
          </div>
        ) : (
          <p className="text-center text-muted-foreground">Please enter a query above.</p>
        )}
      </div>
      <Toaster />
    </main>
  );
}
