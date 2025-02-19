// frontend/app/components/AgentStepsAccordion.tsx

"use client"

import * as React from "react"
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion"

interface AgentStepsAccordionProps {
  stepsString: string
}

export function AgentStepsAccordion({ stepsString }: AgentStepsAccordionProps) {
  // For demonstration, split steps by newlines.
  // If your chain-of-thought is huge, you might want a different approach.
  const lines = stepsString.split("\n").filter((line) => line.trim().length > 0)

  return (
    <Accordion type="multiple" className="w-full">
      {lines.map((line, idx) => (
        <AccordionItem key={idx} value={`step-${idx}`}>
          <AccordionTrigger>Step {idx + 1}</AccordionTrigger>
          <AccordionContent>
            <pre className="bg-muted-foreground/10 p-2 rounded whitespace-pre-wrap text-sm">
              {line}
            </pre>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  )
}
