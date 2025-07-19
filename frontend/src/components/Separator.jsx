import { forwardRef } from "react"
import { cn } from "../utils/cn"

const Separator = forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("shrink-0 bg-gray-200 h-[1px] w-full", className)} {...props} />
))
Separator.displayName = "Separator"

export { Separator }
