// frontend/components/search-results.tsx
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { SearchCheck, ExternalLink, Copy, CheckCircle2, ChevronDown } from "lucide-react";
import { useState } from "react";
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

/**
 * Fallback parser: Extract search links from research_task logs.
 */
function parseSearchLinksFromLogs(lines: string[]): SearchLink[] {
  const links: SearchLink[] = [];
  // Updated regex to capture multi-line output
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
          snippet: "", // Return empty snippet instead of "N/A"
          credibility: "NEWS",
        });
      }
    }
  }
  // Deduplicate links by URL
  const uniqueLinksMap: { [url: string]: SearchLink } = {};
  links.forEach(link => {
    uniqueLinksMap[link.url] = link;
  });
  return Object.values(uniqueLinksMap);
}

export default function SearchResults({ data }: SearchResultsProps) {
  const [copiedUrl, setCopiedUrl] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(true);

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

  let results = data.search_links || [];
  // Fallback: If no search links provided, try to extract them from agentWorkflow logs.
  if (results.length === 0 && data.agentWorkflow && data.agentWorkflow.length > 0) {
    results = parseSearchLinksFromLogs(data.agentWorkflow);
  }

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader className="cursor-pointer select-none" onClick={() => setIsExpanded(!isExpanded)}>
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <SearchCheck className="h-5 w-5 text-primary" />
            Search Results
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {results.length}
            </Badge>
          </div>
          <ChevronDown
            className={cn("h-4 w-4 text-muted-foreground transition-transform duration-200", isExpanded && "rotate-180")}
          />
        </CardTitle>
      </CardHeader>
      {isExpanded && (
        <CardContent className="grid gap-4 transition-all duration-200 p-4">
          {results.length === 0 ? (
            <p className="text-sm text-muted-foreground">No search results found.</p>
          ) : (
            results.map((r, idx) => (
              <div key={idx} className="space-y-2 rounded-lg border border-border/50 p-4 hover:bg-muted/20">
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
                <h3 className="font-semibold text-foreground">{r.title}</h3>
                {r.snippet && r.snippet.trim() !== "" && (
                  <p className="text-sm text-muted-foreground line-clamp-2">{r.snippet}</p>
                )}
              </div>
            ))
          )}
        </CardContent>
      )}
    </Card>
  );
}
