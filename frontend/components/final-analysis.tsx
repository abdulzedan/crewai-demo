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

interface FinalAnalysisProps {
  data: {
    finalAnalysis: {
      summary: string[];
      confidence: number;
    };
  };
}

export default function FinalAnalysis({ data }: FinalAnalysisProps) {
  const [analysisMd, setAnalysisMd] = useState<string>("");
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false); // collapsed by default

  useEffect(() => {
    if (data.finalAnalysis && data.finalAnalysis.summary) {
      let [mdString] = data.finalAnalysis.summary;
      if (mdString.startsWith("```") && mdString.endsWith("```")) {
        mdString = mdString.replace(/^```[\s\S]*?\n/, "").replace(/\n```$/, "");
      }
      setAnalysisMd(mdString || "");
      setIsExpanded(false); // Reset to collapsed when new data arrives.
    }
  }, [data.finalAnalysis]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(analysisMd);
    setCopied(true);
    toast("Analysis copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleClear = () => {
    setAnalysisMd("");
  };

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader className="flex items-center justify-between cursor-pointer" onClick={() => setIsExpanded(!isExpanded)}>
        <CardTitle className="flex items-center gap-2 text-lg font-medium">
          <CheckCircle2 className="h-5 w-5 text-green-400" />
          Final Analysis
        </CardTitle>
        <ChevronDown className={cn("h-5 w-5 text-muted-foreground transition-transform duration-200", isExpanded ? "rotate-180" : "rotate-0")} />
      </CardHeader>
      {isExpanded && (
        <CardContent className="space-y-4 p-4 text-left">
          {analysisMd ? (
            <>
              <div className="prose prose-lg dark:prose-invert max-w-prose p-6 rounded-lg border border-border bg-background shadow-lg">
                <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
                  {analysisMd}
                </ReactMarkdown>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={handleCopy}>
                  {copied ? <CheckCircle2 className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
                  {copied ? "Copied!" : "Copy"}
                </Button>
                <Button variant="outline" size="sm" onClick={handleClear}>
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
