"use client";

import * as React from "react";
import * as SliderPrimitive from "@radix-ui/react-slider";
import { cn } from "@/lib/utils";

interface LinkSliderProps {
  value: number;
  onValueChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
}

const LinkSlider = React.forwardRef<
  React.ElementRef<typeof SliderPrimitive.Root>,
  LinkSliderProps
>(({ value, onValueChange, min = 1, max = 10, step = 1 }, ref) => {
  return (
    // The container is fixed at 800px and centered.
    <div className="mx-auto mt-4" style={{ width: "500px" }}>
      <div className="mb-2 text-sm font-medium text-foreground">
        Number of Links: {value}
      </div>
      <SliderPrimitive.Root
        ref={ref}
        value={[value]}
        min={min}
        max={max}
        step={step}
        onValueChange={(values) => onValueChange(Number(values[0]))}
        // Directly force the slider's width to 800px (remove w-full)
        style={{ width: "500px" }}
        className="relative flex h-4 touch-none select-none items-center"
      >
        <SliderPrimitive.Track className="relative h-2 grow overflow-hidden rounded-full bg-secondary">
          <SliderPrimitive.Range className="absolute h-full bg-primary transition-all duration-300" />
        </SliderPrimitive.Track>
        <SliderPrimitive.Thumb className="block h-4 w-4 rounded-full border-2 border-primary bg-background shadow transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" />
      </SliderPrimitive.Root>
    </div>
  );
});

LinkSlider.displayName = "LinkSlider";

export { LinkSlider };
