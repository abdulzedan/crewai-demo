// frontend/components/agent-workflow.tsx
"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { ChevronDown, MessageSquareText, Activity } from "lucide-react";
import { cn } from "@/lib/utils";
import CollapsibleMarkdown from "@/components/collapsible-markdown";

interface AgentMessage {
  timestamp: string;
  content: string;
}

interface Agent {
  id: string;
  role: string;
  messages: AgentMessage[];
}

interface AgentWorkflowProps {
  data: {
    agentWorkflow: string[];
  };
}

// Updated parser: deduplicate messages with the same content for an agent.
function parseAgentLogs(logLines: string[]): Agent[] {
  const agents: { [agentName: string]: Agent } = {};
  const roleMap: { [key: string]: string } = {
    "Expert Web Researcher": "Researcher",
    "Analytical Aggregator": "Analyzer",
    "Innovative Synthesizer": "Synthesizer",
  };

  const logPattern = /^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}):\s*([\s\S]+)$/;
  const fieldPattern = /(\w+)="([\s\S]*?)"/g;

  for (const line of logLines) {
    const trimmed = line.trim();
    const match = trimmed.match(logPattern);
    if (!match) continue;
    const timestamp = match[1];
    const fieldsStr = match[2];
    const fields: { [key: string]: string } = {};
    let fieldMatch;
    while ((fieldMatch = fieldPattern.exec(fieldsStr)) !== null) {
      fields[fieldMatch[1]] = fieldMatch[2];
    }
    const agentName = fields["agent"];
    if (!agentName) continue;
    if (!agents[agentName]) {
      agents[agentName] = {
        id: agentName,
        role: roleMap[agentName] || agentName,
        messages: [],
      };
    }
    let content = fields["task"] || "";
    if (fields["status"] === "completed" && fields["output"]) {
      content += "\nOutput: " + fields["output"];
    }
    // Deduplicate: only add if no existing message has the same content.
    if (!agents[agentName].messages.some(msg => msg.content === content)) {
      agents[agentName].messages.push({ timestamp, content });
    }
  }
  return Object.values(agents);
}

export default function AgentWorkflow({ data }: AgentWorkflowProps) {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isExpanded, setIsExpanded] = useState(true);

  useEffect(() => {
    if (data.agentWorkflow && Array.isArray(data.agentWorkflow) && data.agentWorkflow.length > 0) {
      const parsedAgents = parseAgentLogs(data.agentWorkflow);
      setAgents(parsedAgents);
    }
  }, [data.agentWorkflow]);

  return (
    <Card className="border-border/50 shadow-lg bg-card/50 backdrop-blur">
      <CardHeader className="cursor-pointer select-none" onClick={() => setIsExpanded(!isExpanded)}>
        <CardTitle className="flex items-center justify-between text-lg font-medium">
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary" />
            Agent Workflow
            <Badge variant="secondary" className="ml-2 bg-secondary/50">
              {agents.length} agents
            </Badge>
          </div>
          <ChevronDown className={cn("h-5 w-5 text-muted-foreground transition-transform duration-200", isExpanded && "rotate-180")} />
        </CardTitle>
      </CardHeader>
      {isExpanded && (
        <CardContent className="transition-all duration-200">
          {agents.length === 0 ? (
            <p className="text-sm text-muted-foreground">No logs available.</p>
          ) : (
            agents.map((agent, idx) => (
              <Accordion type="single" collapsible className="w-full mb-2" key={agent.id + idx}>
                <AccordionItem value={agent.id}>
                  <AccordionTrigger className="hover:no-underline">
                    <div className="flex items-center gap-2 text-sm">
                      <MessageSquareText className="h-4 w-4 text-primary" />
                      <span>{agent.role}</span>
                      <Badge variant="secondary" className="ml-2 bg-secondary/50">
                        {agent.messages.length} messages
                      </Badge>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="space-y-2 pt-4 text-sm text-muted-foreground whitespace-pre-wrap">
                      {agent.messages.map((msg, i) => (
                        <div key={i} className="space-y-1">
                          <time className="block text-xs italic text-gray-400">{msg.timestamp}</time>
                          <CollapsibleMarkdown content={msg.content} lineClamp={2} />
                        </div>
                      ))}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            ))
          )}
        </CardContent>
      )}
    </Card>
  );
}
