"use client";

import { useState, useEffect } from "react";
import { Search, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface SearchBarProps {
  onSearch: (query: string, maxLinks: number) => void;
  loading: boolean;
  onClear: () => void;
}

export default function SearchBar({ onSearch, loading, onClear }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [progress, setProgress] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [internalLoading, setInternalLoading] = useState(loading);
  const [maxLinks, setMaxLinks] = useState<number>(3);

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
    onSearch(query, maxLinks);
  };

  return (
    <div className="space-y-2 w-full max-w-4xl">
      <form onSubmit={handleSearch} className="relative">
        <div className="relative flex w-full">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pr-16 h-16 text-lg bg-background/50 shadow-lg border-border/50 rounded-full backdrop-blur transition-all duration-300"
            placeholder="Ask anything..."
            type="search"
          />
          <div className="absolute right-4 top-2">
            <Button
              size="icon"
              type="submit"
              disabled={internalLoading}
              className="h-12 w-12 rounded-full"
            >
              {internalLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Search className="h-5 w-5" />}
              <span className="sr-only">Search</span>
            </Button>
          </div>
        </div>
        <div className="mt-2">
          <label htmlFor="maxLinks" className="block text-sm font-medium text-muted-foreground">
            Number of Links: {maxLinks}
          </label>
          <input
            id="maxLinks"
            type="range"
            min="1"
            max="10"
            value={maxLinks}
            onChange={(e) => setMaxLinks(Number(e.target.value))}
            className="w-full"
          />
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
