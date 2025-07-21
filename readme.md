# 🛠️ SenaryLabTask: AI-Powered Support Ticket Classifier

A full-stack web application that enables users to submit support tickets, which are then analyzed using OpenAI's API to classify their content and assess urgency.

Built with:

- 🚀 **FastAPI** for the backend
- ⚛️ **React + Vite** for the frontend
- 🧠 **OpenAI GPT** for classification logic

---

## 📖 Overview

The application enables users to submit support tickets via a web form. The submitted data (name, email, issue description, and optional attachments) is sent to a FastAPI backend endpoint. The backend then forwards the ticket text to a custom prompting script that uses OpenAI's API. The response classifies the issue into one of the following categories:

- `Bug Report`
- `Feature Request`
- `Praise/Positive Feedback`
- `General Inquiry`

Additionally, the model assigns an  urgency score between 1 and 5 to bug reports based on this scheme:
`1: Not Urgent`
`2: Low`
`3: Medium`
`4: High`
`5: Critical`
Categories other than Bug report receive an urgency of none.

---


## 🛠️ Features

- Submit support tickets with attachments
- OpenAI-powered classification (category + urgency score)
- CORS-enabled backend API
- Upload and parse text input
- Store ticket and LLM response mapping
- JSON-based configuration and ticket database
UI 
---

## ⚙️ Setup Instructions

### 📁 Prerequisites

- Python 3.10+
- Node.js + npm
- Docker & Docker Compose (optional)

---

## 🔐 Environment Configuration

Before running, **you must set up your environment variables** in a `.env` file in the root directory. The file should include:

- OpenAI credentials
- Path to the config file (either `default_config.json` or `docker_config.json`)

Use `.env.example` as a template:

```env
OPENAI_API_KEY=your_api_key
OPENAI_ORG_ID=your_org_id
OPENAI_PROJECT_ID=your_project_id
CONFIG_PATH=backend/config/default_config.json  # or docker_config.json if using Docker
```
---

## 🚀 Running the Project

There are **two ways** to run this project:

### 🟢 Option 1: Using the Bash Script
1- Set the CONFIG_FILE variable in your env to "backend/config/default_config.json"
```bash
./run_project.sh
```

This script starts both the FastAPI backend and the Vite React frontend from the project root.

### 🐳 Option 2: Using Docker Compose
1- Set the CONFIG_FILE variable in your env to "config/docker_config.json"

2- Build docker container
```bash
docker compose up --build
```

This spins up both services in containers with volumes and port mappings configured.

### ❗ Make sure to configure environment variables in .env before running ❗
## Dashboard
Dashboarrd runs seprately from the project:
1- Go to Dashboard directory: 
```bash
cd dashboard
```
2- Run run_dashboard,sh 
```bash
bash run_dashboard.sh
```
### ❗ Make sure DB_path in default_config of the configuration you're using exists and has data before running the dashboard ❗
---

## 🧲 Running Tests

Backend unit tests are located in the `/backend/tests/` folder.

Run with:

```bash
pytest
```

---
## 📡 Requesting the API Directly

To send requests to Backend 

use this command template:

```curl
  curl -X POST http://localhost:8000/submit-ticket \
  -F "ticket_id=IT-ABC12345" \
  -F "first_name=name" \
  -F "last_name=lastname" \
  -F "email=name@example.com" \
  -F "phone=+971500000000" \
  -F "text= issue description"
```
## 📁 Project Structure

```
SenaryLabTask/
├── backend/
│   ├── src/
│   │   ├── api/  ###Contains fastAPI component & Response Validation
│   │   ├── models/ ### Prompt and Code for Openai API & Prompt Text
│   ├── config/ ### Configuration files
│   │   ├── default_config.json  ##use with local run
│   │   ├── docker_config.json  ##use with docker build
│   ├── tests/ ##backend unit tests
│   │   ├──  conftest.py  ##Test Fast API and OpenAI configuration
│   │   ├── test_main.py ## Multiple test case with different LL outputs
│   └── Dockerfile/

├── frontend/
│   ├── src/ 
│   │   ├── components/  
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── vite.config.mjs

├── run_project.sh
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

---

## ✨ Sample LLM Output Format

The response from the OpenAI API is expected to be in this JSON format:

```json
{
  "feedback_text": "Example text",
  "category": "Bug Report",
  "urgency_score": 3
}
```
---
## 🧪 Input & Output Validation

### ✅ Input Validation

- All ticket submission fields marked as required **must** be provided.
- The `email` field is validated to ensure it follows a standard email format.
- Optional fields like `phone` and file attachments are gracefully handled if missing.
---
### 🧠 LLM Output Validation

The response from the language model is validated to ensure consistent structure and value constraints:

- Must be a JSON object with the following keys:
  - `feedback_text` (string)
  - `category` (string)
  - `urgency_score` (integer between 1 and 5 or null)
- If any required key is missing or the types do not match expectations, a validation error is raised before proceeding.
---
## 🛡️ Model & Engine Error Handling

The backend includes robust error handling to ensure a smooth user experience even when issues occur with the language model or configuration:

- If the `prompt_llm` function fails to load (due to misconfigured script path or missing definition), the API returns a `503 Service Unavailable` status and blocks further ticket submission attempts until resolved.
- If the LLM returns malformed JSON or an error during execution, the system catches the issue and responds with appropriate HTTP error codes (`502` for model errors, `504` for invalid output).
- All unexpected runtime errors are logged via `traceback` and surfaced as `500 Internal Server Error` to aid debugging without exposing sensitive information.
---
## 🎁 Bonus Features

This project includes a few enhanced capabilities to improve model behavior and usability:

- **🎯 Fine-Tuned Few-Shot Prompting**: The LLM is prompted using structured few-shot examples to improve classification reliability across various ticket categories and urgency levels.
- **📁 JSON Ticket History**: All submitted tickets, along with their LLM-generated responses, are stored in a JSON file This enables:
  - Easy auditing of LLM outputs
  - Fine-tuning data collection
  - Offline analysis and reporting
---
## 🔭 Future Improvements 
- Add user login/authentication
- Database integration (PostgreSQL)
- Admin dashboard for ticket management
- Add user limits to prevent spam
---
## 📢 Feedback

For questions or suggestions, feel free to open an issue or reach out.
