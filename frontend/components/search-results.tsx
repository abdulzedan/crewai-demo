"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { SearchCheck, ExternalLink, Copy, CheckCircle2, ChevronDown } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

interface SearchResult {
  url: string;
  title: string;
  snippet: string;
  credibility: string;
}

export default function SearchResults() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [copiedUrl, setCopiedUrl] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(true);

  useEffect(() => {
    // If aggregator returns search links in data.search_links, do:
    // fetch("/api/analysis", {...}).then((res) => res.json()).then((data) => setResults(data.search_links || []))
    // For now, use static data:
    setResults([
      {
        url: "https://www.reuters.com/technology/qatar-signs-deal-with-scale-ai",
        title: "Qatar Partners with Scale AI",
        snippet: "Qatar is leveraging AI to boost government services...",
        credibility: "OK",
      },
      {
        url: "https://www.theregister.com/2025/02/23/aleph_alpha_sovereign_ai",
        title: "Aleph Alpha's Sovereign AI Approach",
        snippet: "Challenges in building enterprise AI apps with large language models...",
        credibility: "NEWS",
      },
    ]);
  }, []);

  const handleCopyUrl = async (url: string) => {
    await navigator.clipboard.writeText(url);
    setCopiedUrl(url);
    setTimeout(() => setCopiedUrl(null), 2000);
  };

  const getCredColor = (cred: string) => {
    switch (cred) {
      case "OK":
        return "bg-green-900/50 text-green-300";
      case "NEWS":
        return "bg-blue-900/50 text-blue-300";
      case "FAKE":
        return "bg-red-900/50 text-red-300";
      default:
        return "bg-gray-900/50 text-gray-300";
    }
  };

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader
        className="cursor-pointer select-none"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <SearchCheck className="h-5 w-5 text-primary" />
            Search Results
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {results.length}
            </Badge>
          </div>
          <ChevronDown
            className={cn(
              "h-4 w-4 text-muted-foreground transition-transform duration-200",
              isExpanded && "transform rotate-180"
            )}
          />
        </CardTitle>
      </CardHeader>
      {isExpanded && (
        <CardContent className="grid gap-4 transition-all duration-200">
          {results.map((r, idx) => (
            <div
              key={idx}
              className="space-y-2 rounded-lg border border-border/50 p-4 hover:bg-muted/20"
            >
              <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="font-mono">{r.url}</span>
                  <Badge variant="secondary" className={getCredColor(r.credibility)}>
                    {r.credibility}
                  </Badge>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="icon" onClick={() => handleCopyUrl(r.url)}>
                    {copiedUrl === r.url ? (
                      <CheckCircle2 className="h-4 w-4 text-green-400" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                    <span className="sr-only">Copy URL</span>
                  </Button>
                  <Button variant="ghost" size="icon" asChild>
                    <a href={r.url} target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-4 w-4" />
                      <span className="sr-only">Open link</span>
                    </a>
                  </Button>
                </div>
              </div>
              <h3 className="font-semibold text-foreground">{r.title}</h3>
              <p className="text-sm text-muted-foreground line-clamp-2">{r.snippet}</p>
            </div>
          ))}
        </CardContent>
      )}
    </Card>
  );
}
