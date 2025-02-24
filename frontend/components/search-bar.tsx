// frontend/components/search-bar.tsx
"use client";

import { useState, useEffect } from "react";
import { Search, Loader2, X } from "lucide-react";
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

  // Sync internal loading with parent's loading prop.
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

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    // Trigger parent's search; parent's loading state will drive internal state.
    onSearch(query);
  };

  const handleClear = () => {
    setQuery("");
    onClear();
  };

  return (
    <div className="space-y-2">
      <form onSubmit={handleSearch} className="relative">
        <div className="relative flex w-full max-w-3xl mx-auto">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pr-24 h-12 bg-background/50 shadow-lg border-border/50 rounded-full backdrop-blur"
            placeholder="Ask anything..."
            type="search"
          />
          <div className="absolute right-1 top-1 flex gap-2">
            {!internalLoading && (
              <Button
                type="button"
                size="icon"
                variant="ghost"
                className="h-10 w-10 rounded-full hover:bg-muted/20"
                onClick={handleClear}
              >
                <X className="h-4 w-4" />
                <span className="sr-only">Clear</span>
              </Button>
            )}
            <Button
              size="icon"
              type="submit"
              disabled={internalLoading}
              className="h-10 w-10 rounded-full"
            >
              {internalLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
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
