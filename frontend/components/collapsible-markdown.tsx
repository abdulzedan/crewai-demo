// frontend/components/collapsible-markdown.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

interface CollapsibleMarkdownProps {
  content: string;
  lineClamp?: number;
}

export default function CollapsibleMarkdown({ content, lineClamp = 3 }: CollapsibleMarkdownProps) {
  const [expanded, setExpanded] = useState(false);
  // Determine if the content needs collapsing based on newline count
  const lines = content.split("\n");
  const needsCollapse = lines.length > lineClamp;

  return (
    <div>
      <div
        className={`transition-all duration-300 ${
          !expanded && needsCollapse ? `line-clamp-${lineClamp}` : ""
        }`}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
          {content}
        </ReactMarkdown>
      </div>
      {needsCollapse && (
        <Button variant="link" size="sm" onClick={() => setExpanded(!expanded)}>
          {expanded ? "Show Less" : "Read More"}
        </Button>
      )}
    </div>
  );
}
