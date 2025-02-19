// frontend/app/chat/page.tsx
"use client"

import React from 'react';
import Link from "next/link";

export default function ChatPage() {
  return (
    <main className="flex h-screen flex-col">
      <header className="flex items-center justify-between bg-white px-4 py-2 shadow-sm">
        <div className="text-lg font-bold">My Writing Assistant</div>
        <div className="space-x-4 text-sm text-gray-600">
          Hello, User
        </div>
      </header>

      <div className="flex h-full flex-1 overflow-hidden">
        {/* Sidebar (optional) */}
        <aside className="hidden w-60 flex-col bg-white p-4 shadow-sm sm:flex">
          <div className="mb-4 text-xl font-semibold text-gray-700">Tools</div>
          <nav className="flex flex-col space-y-2 text-sm">
            <Link href="#" className="rounded bg-gray-200 px-3 py-2 font-medium text-gray-800">
              New Document
            </Link>
            <Link href="#" className="rounded px-3 py-2 text-gray-600 hover:bg-gray-100">
              Saved Documents
            </Link>
            <Link href="#" className="rounded px-3 py-2 text-gray-600 hover:bg-gray-100">
              Past Chats
            </Link>
            <Link href="#" className="rounded px-3 py-2 text-gray-600 hover:bg-gray-100">
              Settings
            </Link>
          </nav>
        </aside>

        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Chat messages and input would be rendered here */}
          <div className="flex flex-1 items-center justify-center">
            <p className="text-lg">This is the Chat Page. Use the main chat UI for conversation.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
