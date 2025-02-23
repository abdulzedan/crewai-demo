// frontend/app/page.tsx
"use client";

import SearchBar from "@/components/search-bar";
import SearchResults from "@/components/search-results";
import AgentWorkflow from "@/components/agent-workflow";
import FinalAnalysis from "@/components/final-analysis";

export default function Page() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-background/50 to-background">
      <div className="container max-w-3xl mx-auto px-4 py-8 space-y-4">
        {/* Search bar */}
        <div className="sticky top-4 z-10 mb-8">
          <SearchBar />
        </div>

        {/* Collapsible cards */}
        <SearchResults />
        <AgentWorkflow />
        <FinalAnalysis />
      </div>
    </main>
  );
}
