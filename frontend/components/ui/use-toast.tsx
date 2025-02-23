// frontend/components/ui/use-toast.tsx
"use client";

import { createContext, useContext, useState, ReactNode } from "react";

interface ToastContextValue {
  toast: (message: string) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

export const ToastProvider = ({ children }: { children: ReactNode }) => {
  const [toasts, setToasts] = useState<string[]>([]);

  const toast = (message: string) => {
    setToasts((prev) => [...prev, message]);
    // For demonstration, log the toast and clear after 2 seconds.
    console.log("Toast:", message);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t !== message));
    }, 2000);
  };

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed bottom-4 right-4 space-y-2">
        {toasts.map((message, index) => (
          <div key={index} className="bg-black text-white p-2 rounded">
            {message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
}
