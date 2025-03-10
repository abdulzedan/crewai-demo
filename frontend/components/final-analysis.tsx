// frontend/components/final-analysis.tsx

"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Copy, Trash2, ChevronDown } from "lucide-react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { cn } from "@/lib/utils";
import { Progress } from "@/components/ui/progress";

interface FinalAnalysisProps {
  data: {
    finalAnalysis?: {
      summary?: string[];
      confidence?: number;
    };
  };
}

export default function FinalAnalysis({ data }: FinalAnalysisProps) {
  const [analysisMd, setAnalysisMd] = useState<string>("");
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    if (data?.finalAnalysis?.summary && Array.isArray(data.finalAnalysis.summary)) {
      const [mdString] = data.finalAnalysis.summary;
      setAnalysisMd(mdString || "");
      setIsExpanded(false);
    }
  }, [data?.finalAnalysis]);

  const handleCopy = () => {
    if (!analysisMd) return;
    navigator.clipboard.writeText(analysisMd);
    setCopied(true);
    toast("Analysis copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleClear = () => {
    setAnalysisMd("");
  };

  const confidence = data?.finalAnalysis?.confidence ?? 0;
  const confidencePercent = Math.round(confidence * 100);

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader
        onClick={() => setIsExpanded(!isExpanded)}
        className="cursor-pointer select-none"
      >
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-green-400" />
            <span>Final Analysis</span>
          </div>
          <ChevronDown
            className={cn(
              "h-5 w-5 text-muted-foreground transition-transform duration-200",
              isExpanded ? "rotate-180" : "rotate-0"
            )}
          />
        </CardTitle>
      </CardHeader>

      {isExpanded && (
        <CardContent className="p-4 space-y-4 text-left">
          {/* Confidence bar */}
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">
              Confidence: {confidencePercent}%
            </span>
            <Progress value={confidencePercent} className="h-2 w-full" />
          </div>

          {analysisMd ? (
            <>
              <div className="prose dark:prose-invert max-w-none text-left p-6 leading-relaxed space-y-2 rounded-lg border border-border bg-background shadow-lg whitespace-pre-wrap break-words">
                <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
                  {analysisMd}
                </ReactMarkdown>
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCopy();
                  }}
                >
                  {copied ? (
                    <>
                      <CheckCircle2 className="h-4 w-4 text-green-400" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                      Copy
                    </>
                  )}
                </Button>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleClear();
                  }}
                >
                  <Trash2 className="h-4 w-4" />
                  Clear
                </Button>
              </div>
            </>
          ) : (
            <p className="text-sm text-muted-foreground">No final analysis yet.</p>
          )}
        </CardContent>
      )}
    </Card>
  );
}
