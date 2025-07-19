"use client"

import { useState } from "react"
import { Button } from "../components/Button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/Card"
import { Input } from "../components/Input"
import { Label } from "../components/Label"
import { Textarea } from "../components/Textarea"
import { Upload, User, MessageSquare } from "../components/Icons"

export default function IssueSubmission() {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    issueDescription: "",
  })

  const [attachments, setAttachments] = useState([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleSystemChange = (system, checked) => {
    setFormData((prev) => ({
      ...prev,
      affectedSystems: checked ? [...prev.affectedSystems, system] : prev.affectedSystems.filter((s) => s !== system),
    }))
  }

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files)
    setAttachments((prev) => [...prev, ...files])
  }

  const removeAttachment = (index) => {
    setAttachments((prev) => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000))

    setIsSubmitting(false)
    setSubmitted(true)
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <CardTitle className="text-green-800">Ticket Submitted Successfully!</CardTitle>
            <CardDescription>
              Your support ticket has been created. You'll receive a confirmation email shortly with your ticket number.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="bg-gray-100 p-3 rounded-lg mb-4">
              <p className="text-sm text-gray-600">Ticket ID</p>
              <p className="font-mono font-bold text-lg">#IT-{Math.random().toString(36).substr(2, 8).toUpperCase()}</p>
            </div>
            <Button
              onClick={() => {
                setSubmitted(false)
                setFormData({
                  firstName: "",
                  lastName: "",
                  email: "",
                  phone: "",
                  issueDescription: "",
                })
                setAttachments([])
              }}
              className="w-full"
            >
              Submit Another Ticket
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">IT Support Request</h1>
          <p className="text-gray-600">Submit a detailed description of your technical issue for faster resolution</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Personal Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="w-5 h-5" />
                Contact Information
              </CardTitle>
              <CardDescription>Please provide your contact details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="firstName">First Name *</Label>
                  <Input
                    id="firstName"
                    value={formData.firstName}
                    onChange={(e) => handleInputChange("firstName", e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="lastName">Last Name *</Label>
                  <Input
                    id="lastName"
                    value={formData.lastName}
                    onChange={(e) => handleInputChange("lastName", e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="email">Email Address *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => handleInputChange("phone", e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Issue Description */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="w-5 h-5" />
                Issue Description
              </CardTitle>
              <CardDescription>Describe the technical issue you're experiencing</CardDescription>
            </CardHeader>
            <CardContent>
              <div>
                <Label htmlFor="issueDescription">Please describe your issue in detail *</Label>
                <Textarea
                  id="issueDescription"
                  placeholder="Please describe the issue in detail, including what you were trying to do when the problem occurred"
                  value={formData.issueDescription}
                  onChange={(e) => handleInputChange("issueDescription", e.target.value)}
                  rows={6}
                  required
                />
              </div>
            </CardContent>
          </Card>

          {/* File Attachments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Attachments
              </CardTitle>
              <CardDescription>Upload screenshots, error logs, or other relevant files (optional)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <div className="space-y-2">
                  <Label htmlFor="file-upload" className="cursor-pointer">
                    <span className="text-blue-600 hover:text-blue-500">Click to upload files</span>
                    <span className="text-gray-500"> or drag and drop</span>
                  </Label>
                  <Input
                    id="file-upload"
                    type="file"
                    multiple
                    onChange={handleFileUpload}
                    className="hidden"
                    accept=".jpg,.jpeg,.png,.gif,.pdf,.txt,.log,.doc,.docx"
                  />
                  <p className="text-xs text-gray-500">PNG, JPG, PDF, TXT, DOC up to 10MB each</p>
                </div>
              </div>

              {attachments.length > 0 && (
                <div className="mt-4 space-y-2">
                  <Label>Attached Files:</Label>
                  {attachments.map((file, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                      <span className="text-sm truncate">{file.name}</span>
                      <Button type="button" variant="ghost" size="sm" onClick={() => removeAttachment(index)}>
                        Remove
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end">
            <Button type="submit" disabled={isSubmitting} className="min-w-[120px]">
              {isSubmitting ? "Submitting..." : "Submit Ticket"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
