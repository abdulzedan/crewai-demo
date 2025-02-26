"use client";

import { useState } from "react";
import SearchBar from "@/components/search-bar";
import { LinkSlider } from "@/components/link-slider";
import SearchResults from "@/components/search-results";
import AgentWorkflow from "@/components/agent-workflow";
import FinalAnalysis from "@/components/final-analysis";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/sonner";
import { Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Page() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [animateOut, setAnimateOut] = useState(false);
  const [linkCount, setLinkCount] = useState<number>(3);

  const handleSearch = (query: string) => {
    setLoading(true);
    fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, linkCount }),
    })
      .then((res) => res.json())
      .then((resData) => {
        setTimeout(() => {
          setData(resData);
          setLoading(false);
        }, 500);
      })
      .catch((err) => {
        console.error("Error fetching analysis data:", err);
        setLoading(false);
      });
  };

  const handleClear = () => {
    setAnimateOut(true);
    setTimeout(() => {
      setData(null);
      setAnimateOut(false);
    }, 500);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-background/50 to-background transition-all duration-500">
      {data ? (
        <div className="container max-w-4xl mx-auto py-4 transition-all duration-500">
          {/* Search bar always visible at the top with slideIn animation */}
          <div id="search-bar-container" className="transition-all duration-500 animate-slideIn">
            <SearchBar onSearch={handleSearch} loading={loading} onClear={() => {}} />
          </div>
          <div className="space-y-4 mt-8 transition-all duration-500">
            <SearchResults data={data} />
            <AgentWorkflow data={data} />
            <FinalAnalysis data={data} />
            <div className="mt-8 flex justify-center">
              <Button variant="outline" onClick={handleClear} className="transition-all duration-300 hover:scale-105">
                New Chat
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center h-screen text-center transition-all duration-500">
          <div id="search-bar-container" className="w-full max-w-[900px] transition-all duration-500">
            <div className="flex flex-col items-center gap-2 mb-4">
              <Sparkles className="h-10 w-10 text-primary" />
              <h1 className="text-4xl font-extrabold bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 bg-clip-text text-transparent animate-fadeIn">
                CrewAI Analysis
              </h1>
            </div>
            <SearchBar onSearch={handleSearch} loading={loading} onClear={() => {}} />
          </div>
          <LinkSlider value={linkCount} onValueChange={setLinkCount} />
          <p className="mt-4 text-muted-foreground">
            Enter your query to start the analysis.
          </p>
        </div>
      )}
      <Toaster />
    </main>
  );
}
