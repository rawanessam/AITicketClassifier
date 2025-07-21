# 🛠️ SenaryLabTask: AI-Powered Support Ticket Classifier

A full-stack web application that enables users to submit support tickets, which are then analyzed using OpenAI's API to classify their content and assess urgency.

Built with:

- 🚀 **FastAPI** for the backend
- ⚛️ **React + Vite** for the frontend
- 🧠 **OpenAI GPT** for classification logic

---

## 📆 Features

- Submit support tickets with attachments
- OpenAI-powered classification (category + urgency score)
- CORS-enabled backend API
- Upload and parse text input
- Store ticket and LLM response mapping
- JSON-based configuration and ticket database

---

## ⚙️ Setup Instructions

### 📁 Prerequisites

- Python 3.10+
- Node.js + npm
- Docker & Docker Compose (optional)

---

## 🚀 Running the Project

There are **two ways** to run this project:

### 🟢 Option 1: Using the Bash Script

```bash
./run_project.sh
```

This script starts both the FastAPI backend and the Vite React frontend from the project root.

### 🐳 Option 2: Using Docker Compose

```bash
docker compose up --build
```

This spins up both services in containers with volumes and port mappings configured.

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

## 🧲 Running Tests

Backend unit tests are located in the `/backend/tests/` folder.

Run with:

```bash
pytest
```

---
##  Reuesting API Directly 

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
│   │   ├── api/  ###Contains fastAPI component
│   │   ├── models/ ### Prompt and Code for Openai API
│   ├── config/ ### Configuration files
│   │   ├── default_config.json 
│   │   ├── docker_config.json
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

## 🎁 Bonus Features

This project includes a few enhanced capabilities to improve model behavior and usability:

- **🎯 Fine-Tuned Few-Shot Prompting**: The LLM is prompted using structured few-shot examples to improve classification reliability across various ticket categories and urgency levels.
- **📁 JSON Ticket History**: All submitted tickets, along with their LLM-generated responses, are stored in a JSON file This enables:
  - Easy auditing of LLM outputs
  - Fine-tuning data collection
  - Offline analysis and reporting
-------

## 📢 Feedback

For questions or suggestions, feel free to open an issue or reach out.

