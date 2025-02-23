"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { SearchCheck, ExternalLink, Copy, CheckCircle2, ChevronDown } from "lucide-react"
import { useState } from "react"
import { useToast } from "@/components/ui/use-toast"
import { cn } from "@/lib/utils"

interface SearchResult {
  url: string
  title: string
  snippet: string
  credibility: "OK" | "NEWS" | "FAKE"
}

// In a real implementation, you would fetch search results from your backend API.
// Here we use mock data for demonstration.
const mockResults: SearchResult[] = [
  {
    url: "example.com/article1",
    title: "Understanding AI Agents",
    snippet: "An in-depth look at how AI agents work together to process and analyze information...",
    credibility: "OK",
  },
  {
    url: "example.com/article2",
    title: "The Future of Search",
    snippet: "How modern search engines are evolving with AI integration...",
    credibility: "NEWS",
  },
]

export default function SearchResults() {
  const { toast } = useToast()
  const [copiedUrl, setCopiedUrl] = useState<string | null>(null)
  const [isExpanded, setIsExpanded] = useState(true)

  const handleCopyUrl = async (url: string) => {
    await navigator.clipboard.writeText(url)
    setCopiedUrl(url)
    toast({
      title: "URL copied to clipboard",
      duration: 2000,
    })
    setTimeout(() => setCopiedUrl(null), 2000)
  }

  const getCredibilityColor = (credibility: SearchResult["credibility"]) => {
    switch (credibility) {
      case "OK":
        return "bg-green-900/50 text-green-300"
      case "NEWS":
        return "bg-blue-900/50 text-blue-300"
      case "FAKE":
        return "bg-red-900/50 text-red-300"
      default:
        return "bg-gray-900/50 text-gray-300"
    }
  }

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader className="cursor-pointer select-none" onClick={() => setIsExpanded(!isExpanded)}>
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <SearchCheck className="h-5 w-5 text-primary" />
            Search Results
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {mockResults.length}
            </Badge>
          </div>
          <ChevronDown
            className={cn(
              "h-4 w-4 text-muted-foreground transition-transform duration-200",
              isExpanded && "transform rotate-180",
            )}
          />
        </CardTitle>
      </CardHeader>
      <CardContent className={cn("grid gap-4 transition-all duration-200", !isExpanded && "hidden")}>
        {mockResults.map((result, index) => (
          <div
            key={index}
            className="group relative space-y-2 rounded-lg border border-border/50 p-4 hover:bg-muted/20"
          >
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="font-mono">{result.url}</span>
                <Badge variant="secondary" className={getCredibilityColor(result.credibility)}>
                  {result.credibility}
                </Badge>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 hover:bg-muted/20"
                  onClick={() => handleCopyUrl(result.url)}
                >
                  {copiedUrl === result.url ? (
                    <CheckCircle2 className="h-4 w-4 text-green-400" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                  <span className="sr-only">Copy URL</span>
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted/20" asChild>
                  <a href={`https://${result.url}`} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-4 w-4" />
                    <span className="sr-only">Open link</span>
                  </a>
                </Button>
              </div>
            </div>
            <h3 className="font-semibold text-foreground">{result.title}</h3>
            <p className="text-sm text-muted-foreground line-clamp-2">{result.snippet}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
