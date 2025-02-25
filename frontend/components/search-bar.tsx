"use client";

import { useState, useEffect } from "react";
import { Search, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface SearchBarProps {
  onSearch: (query: string) => void;
  loading: boolean;
  onClear: () => void;
}

export default function SearchBar({ onSearch, loading, onClear }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [progress, setProgress] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [internalLoading, setInternalLoading] = useState(loading);

  useEffect(() => {
    setInternalLoading(loading);
    if (!loading) {
      setProgress(0);
      setElapsedTime(0);
    }
  }, [loading]);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (internalLoading) {
      timer = setInterval(() => {
        setElapsedTime((prev) => prev + 1);
        setProgress((prev) => Math.min(prev + Math.random() * 2, 99));
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [internalLoading]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    document.getElementById("search-bar-container")?.classList.add("animate-slideOut");
    setTimeout(() => {
      onSearch(query);
    }, 500);
  };

  return (
    <div
      id="search-bar-container"
      className="w-full max-w-[900px] space-y-2 transition-all duration-500 mx-auto"
    >
      <form onSubmit={handleSearch} className="relative">
        <div className="relative flex w-full">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pr-20 h-16 text-lg bg-background/50 shadow-lg border-border/50 rounded-full backdrop-blur transition-all duration-300"
            placeholder="Ask anything..."
            type="search"
          />
          <div className="absolute right-4 top-2 flex items-center gap-2">
            <Button
              size="icon"
              type="submit"
              disabled={internalLoading}
              className="h-12 w-12 rounded-full"
            >
              {internalLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Search className="h-5 w-5" />
              )}
              <span className="sr-only">Search</span>
            </Button>
          </div>
        </div>
      </form>
      {internalLoading && (
        <div className="space-y-2">
          <Progress value={progress} className="h-1" />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Processing query...</span>
            <span>{elapsedTime}s elapsed</span>
          </div>
        </div>
      )}
    </div>
  );
}
