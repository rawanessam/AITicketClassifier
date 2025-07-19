"use client"

import { forwardRef } from "react"
import { cn } from "../utils/cn"

const Checkbox = forwardRef(({ className, onCheckedChange, ...props }, ref) => {
  return (
    <input
      type="checkbox"
      className={cn("h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-600", className)}
      ref={ref}
      onChange={(e) => onCheckedChange?.(e.target.checked)}
      {...props}
    />
  )
})
Checkbox.displayName = "Checkbox"

export { Checkbox }
