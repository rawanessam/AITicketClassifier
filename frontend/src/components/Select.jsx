"use client"

import { useState, Children, cloneElement } from "react"
import { cn } from "../utils/cn"

const Select = ({ children, value, onValueChange }) => {
  return (
    <div className="relative">{Children.map(children, (child) => cloneElement(child, { value, onValueChange }))}</div>
  )
}

const SelectTrigger = ({ className, children, value, onValueChange, ...props }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [displayValue, setDisplayValue] = useState("")

  const handleItemSelect = (selectedValue, selectedLabel) => {
    onValueChange?.(selectedValue)
    setDisplayValue(selectedLabel)
    setIsOpen(false)
  }

  return (
    <>
      <button
        type="button"
        className={cn(
          "flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className,
        )}
        onClick={() => setIsOpen(!isOpen)}
        {...props}
      >
        <span className={displayValue ? "text-gray-900" : "text-gray-500"}>{displayValue || children}</span>
        <svg className="h-4 w-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {isOpen && (
        <div className="absolute top-full left-0 right-0 z-50 mt-1 rounded-md border bg-white shadow-lg">
          <div className="py-1">
            {Children.map(
              Children.toArray(props.children).find((child) => child.type === SelectContent)?.props.children,
              (child) =>
                cloneElement(child, {
                  onSelect: handleItemSelect,
                }),
            )}
          </div>
        </div>
      )}
    </>
  )
}

const SelectValue = ({ placeholder }) => {
  return <span className="text-gray-500">{placeholder}</span>
}

const SelectContent = ({ children }) => {
  return <>{children}</>
}

const SelectItem = ({ value, children, onSelect }) => {
  return (
    <div className="px-3 py-2 text-sm hover:bg-gray-100 cursor-pointer" onClick={() => onSelect?.(value, children)}>
      {children}
    </div>
  )
}

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem }
