"use client"

import type React from "react"
import { useState } from "react"
import { Search, Loader2 } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function SearchBar() {
  const [isLoading, setIsLoading] = useState(false)
  const [query, setQuery] = useState("")

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    // Here you would typically trigger an API call to your backend.
    // For demonstration, we simulate a delay.
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setIsLoading(false)
    // Optionally, save the query to a global state or context for use in other components.
  }

  return (
    <form onSubmit={handleSearch} className="relative">
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
        <div className="absolute bottom-0 left-0 h-0.5 w-full overflow-hidden">
          <div className="w-full h-full bg-primary/10">
            <div className="h-full w-1/3 bg-primary animate-[loading_1s_ease-in-out_infinite]" />
          </div>
        </div>
      )}
    </form>
  )
}
