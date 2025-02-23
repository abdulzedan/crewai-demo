"use client"

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { MessageSquareText, Activity } from "lucide-react"
import { useState, useEffect } from "react"
import { ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

interface AgentMessage {
  timestamp: string
  content: string
}

interface Agent {
  id: string
  role: string
  messages: AgentMessage[]
  analysis: string
}

export default function AgentWorkflow() {
  const [agentWorkflow, setAgentWorkflow] = useState<Agent[]>([])
  const [isExpanded, setIsExpanded] = useState(true)

  // Fetch agent workflow logs from the analysis endpoint.
  // Replace "sample query" with the actual query from your app context if needed.
  useEffect(() => {
    fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: "What is the latest in AI" })
    })
      .then(res => res.json())
      .then(data => {
        if (data.agentWorkflow) {
          setAgentWorkflow(data.agentWorkflow);
        }
      })
      .catch(err => console.error("Error fetching agent workflow:", err));
  }, []);

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader className="cursor-pointer select-none" onClick={() => setIsExpanded(!isExpanded)}>
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary" />
            Agent Workflow
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {agentWorkflow.length > 0 ? agentWorkflow.length : "—"}
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
      <CardContent className={cn("transition-all duration-200", !isExpanded && "hidden")}>
        <Accordion type="single" collapsible className="w-full">
          {agentWorkflow.map((agent: Agent, idx) => (
            <AccordionItem key={agent.id || idx} value={agent.id || `agent-${idx}`}>
              <AccordionTrigger className="hover:no-underline">
                <div className="flex items-center gap-2">
                  <MessageSquareText className="h-4 w-4 text-primary" />
                  <span>{agent.role}</span>
                  <Badge variant="secondary" className="ml-2 bg-secondary/50">
                    {agent.messages ? agent.messages.length : 0} messages
                  </Badge>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4 pt-4">
                  <div className="space-y-2">
                    {agent.messages &&
                      agent.messages.map((message: AgentMessage, index: number) => (
                        <div key={index} className="flex items-start gap-2 text-sm">
                          <span className="font-mono text-xs text-muted-foreground">{message.timestamp}</span>
                          <span className="text-muted-foreground">{message.content}</span>
                        </div>
                      ))}
                  </div>
                  <div className="rounded-lg bg-muted/20 p-4">
                    <p className="text-sm font-medium">Analysis</p>
                    <p className="mt-2 font-mono text-sm text-muted-foreground">{agent.analysis}</p>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
    </Card>
  )
}
