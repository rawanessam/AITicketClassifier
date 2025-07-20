import { Children, cloneElement } from "react"
import { forwardRef } from "react"
import { cn } from "../utils/cn"

const RadioGroup = ({ children, value, onValueChange, className, ...props }) => {
  return (
    <div className={cn("grid gap-2", className)} {...props}>
      {Children.map(children, (child) =>
        cloneElement(child, {
          name: "radio-group",
          checked: child.props.value === value,
          onChange: () => onValueChange?.(child.props.value),
        }),
      )}
    </div>
  )
}

const RadioGroupItem = forwardRef(({ className, ...props }, ref) => {
  return (
    <input
      type="radio"
      className={cn("h-4 w-4 border-gray-300 text-blue-600 focus:ring-blue-600", className)}
      ref={ref}
      {...props}
    />
  )
})
RadioGroupItem.displayName = "RadioGroupItem"

export { RadioGroup, RadioGroupItem }
