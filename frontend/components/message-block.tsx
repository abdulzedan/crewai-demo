// frontend/app/components/message-block.tsx
"use client"

import { motion } from "framer-motion"
import type { Message } from "ai"
import { cn } from "@/lib/utils"
import { FuturisticThinking } from "./futuristic-thinking"
import { AgentStepsAccordion } from "./AgentStepsAccordion"

// Extend the default Message type to include "assistant-steps"
type ExtendedMessage = Omit<Message, "role"> & {
  role: "system" | "user" | "assistant" | "data" | "assistant-steps"
}

interface MessageBlockProps {
  message: Message
  isThinking?: boolean
}

export function MessageBlock({ message, isThinking }: MessageBlockProps) {
  const extMessage = message as ExtendedMessage
  const isUser = extMessage.role === "user"
  const isSteps = extMessage.role === "assistant-steps"

  // Left-align the "thinking" bubble so it's not floating in the center.
  if (isThinking) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex w-full justify-start"
      >
        <div className="max-w-[80%] bg-muted p-6 flex flex-col items-start">
          <span className="text-sm font-medium mb-2">AI is processing</span>
          <FuturisticThinking />
        </div>
      </motion.div>
    )
  }

  // Collapsible steps
  if (isSteps) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex w-full justify-start"
      >
        <div className="max-w-[80%] bg-muted p-4 rounded-lg">
          <AgentStepsAccordion stepsString={extMessage.content} />
        </div>
      </motion.div>
    )
  }

  // Normal user/assistant messages
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}
    >
      <div
        className={cn(
          "max-w-[80%] p-4 rounded-lg",
          isUser ? "bg-primary text-primary-foreground" : "bg-muted"
        )}
      >
        <div className="prose dark:prose-invert whitespace-pre-wrap">
          {extMessage.content}
        </div>
      </div>
    </motion.div>
  )
}
