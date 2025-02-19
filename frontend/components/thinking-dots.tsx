export function ThinkingDots() {
  return (
    <div className="flex items-center space-x-1">
      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:-0.3s]" />
      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:-0.15s]" />
      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce" />
    </div>
  );
}
