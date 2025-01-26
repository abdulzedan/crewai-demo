// frontend/components/ChatBot.tsx

'use client'

import React, { useState, FormEvent } from 'react'
import axios from 'axios'
import { Send } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'

// Each pipeline step from the backend
interface PipelineStep {
  role: string
  color: string
  content: string
}

// The /api/chat returns { steps: PipelineStep[] }
interface StepsResponse {
  steps: PipelineStep[]
}

// But your local message structure can store optional color
interface Message {
  role: 'user' | 'assistant'
  content: string
  color?: string
}

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    // user message
    const userMsg: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])

    try {
      // The route returns {steps: PipelineStep[]}
      const resp = await axios.post<StepsResponse>(
        'http://localhost:8000/api/chat',
        { message: input }
      )
      // For each pipeline step, create an assistant message
      const pipelineSteps = resp.data.steps

      const newMessages: Message[] = pipelineSteps.map((step) => ({
        role: 'assistant',
        content: `${step.role}:\n\n${step.content}`,
        color: step.color,
      }))

      // push them
      setMessages((prev) => [...prev, ...newMessages])
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || 'Something went wrong.')
    } finally {
      setLoading(false)
      setInput('')
    }
  }

  return (
    <div className="flex h-full flex-col bg-gray-100 p-4">
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col overflow-hidden rounded-lg bg-white shadow">
        {/* Header */}
        <div className="bg-primary p-4">
          <h1 className="text-2xl font-bold text-primary-foreground">Modern Chatbot</h1>
        </div>

        {/* Messages area */}
        <ScrollArea className="flex-grow p-4 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`${
                msg.role === 'user' ? 'text-right' : 'text-left'
              }`}
            >
              <div
                className="inline-block rounded-lg p-3"
                style={{
                  backgroundColor: msg.role === 'assistant' && msg.color ? msg.color : 'var(--muted)',
                  color: msg.role === 'assistant' && msg.color ? 'black' : undefined,
                }}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="text-left">
              <div className="inline-block rounded-lg bg-muted p-3">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </ScrollArea>

        {/* Input form */}
        <div className="border-t p-4">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me for something..."
              className="flex-grow"
              disabled={loading}
            />
            <Button type="submit" disabled={loading || !input.trim()}>
              <Send className="h-4 w-4" />
            </Button>
          </form>
          {error && (
            <p className="mt-2 text-sm text-red-600">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
