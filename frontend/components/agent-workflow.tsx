"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";

export default function AgentWorkflow() {
  const [workflowLogs, setWorkflowLogs] = useState<string[]>([]);
  const [isExpanded, setIsExpanded] = useState(true);

  useEffect(() => {
    fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: "What is the latest in AI" }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.agentWorkflow) {
          setWorkflowLogs(data.agentWorkflow);
        }
      })
      .catch((err) => console.error("Error fetching agent workflow:", err));
  }, []);

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader
        className="cursor-pointer select-none"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary" />
            Agent Workflow
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {workflowLogs.length} steps
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
        <CardContent className="space-y-4 transition-all duration-200">
          {workflowLogs.length > 0 ? (
            workflowLogs.map((md, idx) => (
              <div key={idx} className="rounded-lg bg-muted/20 p-4 text-sm text-muted-foreground">
                <ReactMarkdown>{md}</ReactMarkdown>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted-foreground">No workflow logs yet.</p>
          )}
        </CardContent>
      )}
    </Card>
  );
}
