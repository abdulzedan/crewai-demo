"use client";

import { useChat } from "ai/react";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Moon, Sun, MessageSquare } from "lucide-react";
import { MessageBlock } from "@/components/message-block";
import Link from "next/link";

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
  });
  const [theme, setTheme] = useState("dark");

  // Initialize theme
  useEffect(() => {
    document.documentElement.classList.add(theme);
    return () => {
      document.documentElement.classList.remove(theme);
    };
  }, [theme]);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    document.documentElement.classList.remove(theme);
    document.documentElement.classList.add(newTheme);
    setTheme(newTheme);
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-background border-r border-border p-4">
        <div className="flex items-center gap-2 mb-8">
          <MessageSquare className="w-6 h-6" />
          <span className="font-semibold text-lg">Chat</span>
        </div>
        <Link href="/" className="flex items-center gap-2 p-2 rounded-lg hover:bg-muted transition-colors">
          <MessageSquare className="w-4 h-4" />
          <span>New Chat</span>
        </Link>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <header className="border-b border-border p-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold">Chat</h1>
          <Button variant="ghost" size="icon" onClick={toggleTheme}>
            {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>
        </header>

        <div className="flex-1 overflow-auto p-4 space-y-4">
          {messages.map((message) => (
            <MessageBlock key={message.id} message={message} />
          ))}
          {isLoading && (
            <MessageBlock
              message={{ id: "loading", role: "assistant", content: "" }}
              isThinking={true}
            />
          )}
        </div>

        <div className="border-t border-border p-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={input}
              onChange={handleInputChange}
              placeholder="Type your message..."
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading}>
              Send
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
