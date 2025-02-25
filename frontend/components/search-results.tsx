// frontend/components/search-results.tsx
"use client";

import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  SearchCheck,
  ExternalLink,
  Copy,
  CheckCircle2,
  ChevronUp,
  ChevronDown,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SearchLink {
  url: string;
  title: string;
  snippet: string;
  credibility: string;
}

interface SearchResultsProps {
  data: {
    search_links: SearchLink[];
    agentWorkflow?: string[];
  };
}

function parseSearchLinksFromLogs(lines: string[]): SearchLink[] {
  const links: SearchLink[] = [];
  const researchRegex = /task_name="research_task"[\s\S]*?status="completed"[\s\S]*?output="([\s\S]*?)"/i;
  for (const line of lines) {
    const match = line.match(researchRegex);
    if (match) {
      const outputText = match[1];
      const urlMatch = outputText.match(/URL:\s*(https?:\/\/\S+)/i);
      const titleMatch = outputText.match(/Title:\s*(.+)/i);
      if (urlMatch) {
        links.push({
          url: urlMatch[1],
          title: titleMatch ? titleMatch[1].trim() : "Untitled",
          snippet: "",
          credibility: "NEWS",
        });
      }
    }
  }
  // Deduplicate by URL
  return Array.from(new Map(links.map((item) => [item.url, item])).values());
}

export default function SearchResults({ data }: SearchResultsProps) {
  const [copiedUrl, setCopiedUrl] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(true);
  const sliderRef = useRef<HTMLDivElement>(null);
  const [sliderProgress, setSliderProgress] = useState(0);

  let results = data.search_links || [];
  if (results.length === 0 && data.agentWorkflow && data.agentWorkflow.length > 0) {
    results = parseSearchLinksFromLogs(data.agentWorkflow);
  }
  results = Array.from(new Map(results.map((item) => [item.url, item])).values());

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

  const scrollUp = () => {
    if (sliderRef.current) {
      sliderRef.current.scrollBy({ top: -300, behavior: "smooth" });
    }
  };

  const scrollDown = () => {
    if (sliderRef.current) {
      sliderRef.current.scrollBy({ top: 300, behavior: "smooth" });
    }
  };

  // Update sliderProgress based on scroll position
  useEffect(() => {
    const sliderElem = sliderRef.current;
    if (!sliderElem) return;
    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = sliderElem;
      const progress = (scrollTop / (scrollHeight - clientHeight)) * 100;
      setSliderProgress(progress);
    };
    sliderElem.addEventListener("scroll", handleScroll);
    return () => sliderElem.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader onClick={() => setIsExpanded(!isExpanded)} className="cursor-pointer select-none">
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <SearchCheck className="h-5 w-5 text-primary" />
            Search Results
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {results.length}
            </Badge>
          </div>
          <ChevronDown
            className={cn("h-5 w-5 text-muted-foreground transition-transform duration-200", isExpanded ? "rotate-0" : "rotate-180")}
          />
        </CardTitle>
      </CardHeader>
      {isExpanded && (
        <CardContent className="p-4 relative">
          {results.length === 0 ? (
            <p className="text-sm text-muted-foreground">No search results found.</p>
          ) : (
            <>
              <div className="absolute right-0 top-0 h-full w-2 bg-gray-300 rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary transition-all duration-300"
                  style={{ transform: `translateY(${sliderProgress}%)` }}
                />
              </div>
              <div className="relative">
                <div className="flex flex-col items-center justify-between mb-2">
                  <Button variant="ghost" size="icon" onClick={scrollUp}>
                    <ChevronUp className="h-5 w-5" />
                    <span className="sr-only">Previous</span>
                  </Button>
                  <Button variant="ghost" size="icon" onClick={scrollDown}>
                    <ChevronDown className="h-5 w-5" />
                    <span className="sr-only">Next</span>
                  </Button>
                </div>
                <div
                  ref={sliderRef}
                  className="flex flex-col space-y-4 overflow-y-auto scroll-smooth snap-y snap-mandatory transition-all duration-500 ease-in-out"
                  style={{ maxHeight: "500px" }}
                >
                  {results.map((r, idx) => (
                    <div
                      key={idx}
                      className="min-h-[120px] flex-shrink-0 snap-center space-y-2 rounded-lg border border-border/50 p-4 hover:bg-muted/20 transition-all duration-300"
                    >
                      <div className="flex items-center justify-between gap-4">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <span className="font-mono break-all">{r.url}</span>
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
                      <h3 className="font-semibold text-foreground hover:text-primary transition-colors duration-200">
                        {r.title}
                      </h3>
                      {r.snippet && r.snippet.trim() !== "" && (
                        <p className="text-sm text-muted-foreground line-clamp-2">{r.snippet}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </CardContent>
      )}
    </Card>
  );
}
