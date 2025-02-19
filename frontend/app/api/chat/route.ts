// frontend/app/api/chat/route.ts

import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();
    console.log("Received messages from client:", messages);

    const userMessage = messages[messages.length - 1]?.content;
    if (!userMessage) {
      return NextResponse.json(
        { error: "No user message provided" },
        { status: 400 }
      );
    }

    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
    console.log("Forwarding message to backend:", `${backendUrl}/api/chat/`);

    const response = await fetch(`${backendUrl}/api/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage })
    });

    console.log("Backend response status:", response.status);

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error received from backend:", errorData);
      return NextResponse.json(
        { error: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log("Backend response data:", data);

    // data => { status: "completed", result: "...", steps: "..." }
    const assistantMessage = {
      id: "assistant-message",
      role: "assistant",
      content: data.result || data.error || "No response from backend"
    };

    const stepsMessage = {
      id: "assistant-steps",
      role: "assistant-steps",
      content: data.steps || ""
    };

    return NextResponse.json({ messages: [assistantMessage, stepsMessage] });
  } catch (error: any) {
    console.error("Error in API route:", error);
    return NextResponse.json(
      { error: error.message || "An error occurred" },
      { status: 500 }
    );
  }
}
