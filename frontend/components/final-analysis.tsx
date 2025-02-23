"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { CheckCircle2, Copy } from "lucide-react"
import { useState, useEffect } from "react"
import { useToast } from "@/components/ui/use-toast"

export default function FinalAnalysis() {
  const { toast } = useToast()
  const [copied, setCopied] = useState(false)
  const [analysis, setAnalysis] = useState<{ summary: string[]; confidence: number }>({
    summary: [],
    confidence: 0,
  })

  useEffect(() => {
    // Fetch final analysis from the analysis endpoint.
    fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: "What is the latest in AI" })
    })
      .then(res => res.json())
      .then(data => {
        if (data.finalAnalysis) {
          setAnalysis(data.finalAnalysis);
        }
      })
      .catch(err => console.error("Error fetching final analysis:", err));
  }, []);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(analysis.summary.join("\n"))
    setCopied(true)
    toast({
      title: "Analysis copied to clipboard",
      duration: 2000,
    })
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg font-medium">
            <CheckCircle2 className="h-5 w-5 text-green-400" />
            Final Analysis
          </CardTitle>
          <Button variant="outline" size="sm" className="gap-2 border-border/50" onClick={handleCopy}>
            {copied ? <CheckCircle2 className="h-4 w-4 text-green-400" /> : <Copy className="h-4 w-4" />}
            {copied ? "Copied!" : "Copy"}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <ul className="list-disc space-y-2 pl-5">
            {analysis.summary.map((point, index) => (
              <li key={index} className="text-muted-foreground">
                {point}
              </li>
            ))}
          </ul>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span className="font-medium">Confidence Score:</span>
            <span className="font-mono">{(analysis.confidence * 100).toFixed(1)}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
