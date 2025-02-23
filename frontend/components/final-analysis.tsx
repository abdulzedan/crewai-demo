"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Copy, ChevronDown } from "lucide-react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";

export default function FinalAnalysis() {
  const [analysisMd, setAnalysisMd] = useState<string>("");
  const [isExpanded, setIsExpanded] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: "What is the latest in AI" }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.finalAnalysis && data.finalAnalysis.summary) {
          // Suppose summary is an array of strings, each is Markdown
          const [mdString] = data.finalAnalysis.summary;
          setAnalysisMd(mdString || "");
        }
      })
      .catch((err) => console.error("Error fetching final analysis:", err));
  }, []);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(analysisMd);
    setCopied(true);
    toast("Analysis copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader
        className="cursor-pointer select-none"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-green-400" />
            Final Analysis
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
        <CardContent className="space-y-4 transition-all duration-200">
          {analysisMd ? (
            <>
              <div className="prose dark:prose-invert">
                <ReactMarkdown>{analysisMd}</ReactMarkdown>
              </div>
              <Button variant="outline" size="sm" onClick={handleCopy}>
                {copied ? <CheckCircle2 className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
                {copied ? "Copied!" : "Copy"}
              </Button>
            </>
          ) : (
            <p className="text-sm text-muted-foreground">No final analysis yet.</p>
          )}
        </CardContent>
      )}
    </Card>
  );
}
