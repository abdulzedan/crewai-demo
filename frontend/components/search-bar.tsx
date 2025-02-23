"use client";

import { useState, useRef, useEffect } from "react";
import { Search, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function SearchBar() {
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [progress, setProgress] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const controllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    let timer: number | null = null;
    if (isLoading && startTime) {
      timer = window.setInterval(() => {
        setProgress((p) => (p < 95 ? p + 5 : p));
        setElapsedSeconds(Math.floor((Date.now() - startTime) / 1000));
      }, 500);
    }
    return () => {
      if (timer !== null) clearInterval(timer);
    };
  }, [isLoading, startTime]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setProgress(0);
    setElapsedSeconds(0);
    setStartTime(Date.now());
    controllerRef.current = new AbortController();

    try {
      const res = await fetch("/api/analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
        signal: controllerRef.current.signal,
      });
      // Optionally parse the result
      await res.json();
      setProgress(100);
    } catch (err) {
      console.error("Search aborted or failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = () => {
    if (controllerRef.current) {
      controllerRef.current.abort();
    }
    setIsLoading(false);
    setProgress(0);
  };

  return (
    <form onSubmit={handleSearch} className="relative space-y-2">
      <div className="relative flex w-full max-w-3xl mx-auto">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pr-12 h-12 bg-background/50 shadow-lg border-border/50 rounded-full backdrop-blur"
          placeholder="Ask anything..."
          type="search"
        />
        <Button
          size="icon"
          type="submit"
          disabled={isLoading || !query.trim()}
          className="absolute right-1 top-1 h-10 w-10 rounded-full"
        >
          {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
          <span className="sr-only">Search</span>
        </Button>
      </div>

      {isLoading && (
        <div className="relative w-full bg-primary/20 rounded h-2 overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-200"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {isLoading && (
        <div className="flex items-center gap-4">
          <Button variant="destructive" onClick={handleStop}>
            Stop
          </Button>
          <span className="text-sm text-muted-foreground">
            Time elapsed: {elapsedSeconds}s
          </span>
        </div>
      )}
    </form>
  );
}
