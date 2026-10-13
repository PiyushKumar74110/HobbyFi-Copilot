# HobbyFi Copilot

**An AI-powered CRM copilot for vendors, built with LLMs, tool-based execution, Retrieval-Augmented Generation (RAG), and human-in-the-loop approval workflows.**

HobbyFi Copilot enables vendors to interact with CRM data through natural-language queries. It connects large language models with structured business tools to support customer lookup, membership management, payment analytics, and controlled business operations.

## Features

- **Natural-language CRM queries** — Retrieve customer, membership, and payment information through conversational prompts.
- **Agentic execution** — Uses planning and tool-based execution to route requests to application functions.
- **Retrieval-Augmented Generation (RAG)** — Retrieves relevant contextual information to support grounded responses.
- **Conversation memory** — Maintains conversation history to support follow-up questions.
- **Vendor authentication** — Uses JWT-based authentication to identify the logged-in vendor.
- **Membership and trial management** — Supports membership-related queries and trial-extension workflows.
- **Approval workflow** — Routes supported business-changing actions through an approval step.
- **Revenue analytics** — Provides access to payment and revenue-related information.
- **Multiple LLM providers** — Supports Google Gemini in production and Ollama for local development.
- **Full-stack deployment** — Backend and frontend deployed using Render, with PostgreSQL hosted on Neon.

## Architecture

```text
Vendor
  |
  v
React + TypeScript Frontend
  |
  v
FastAPI Backend
  |
  v
JWT Authentication
  |
  v
Agent Orchestrator
  |
  +--------------------+
  |                    |
  v                    v
LLM Planner          RAG Retriever
  |
  v
Tool Registry
  |
  +--------------------+
  |         |          |
  v         v          v
 CRM     Membership   Payments
 Tools      Tools     & Analytics
  |
  v
Approval Workflow
(for supported write operations)
  |
  v
Neon PostgreSQL
```

## Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, FastAPI, LangChain |
| Frontend | React, TypeScript |
| LLMs | Google Gemini, Ollama |
| AI architecture | Agent orchestration, tool calling, RAG |
| Database | PostgreSQL, Neon |
| Local database / migration source | SQLite |
| Authentication | JWT |
| Deployment | Render |
| Development tools | Git, GitHub, VS Code |

## How It Works

1. A vendor logs in and receives an authentication token.
2. The vendor submits a natural-language request through the chat interface.
3. The orchestrator processes the request and determines the appropriate execution path.
4. The application retrieves contextual information or invokes a registered business tool.
5. The result is returned to the LLM or formatted for the user, depending on the workflow.
6. Supported write operations can enter an approval workflow before execution.
7. Conversation history is saved to support subsequent interactions.

## Example Queries

```text
Find user HF1001.
```

```text
Show me the membership of HF1001.
```

```text
Show me all trial users.
```

```text
Show me today's revenue.
```

```text
Extend the trial of HF1001.
```

The available results depend on the logged-in vendor, the records in the database, and the tools registered in the application.

## Project Structure

```text
HobbyFi-Copilot/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── orchestrator.py
│   │   │   ├── planner.py
│   │   │   └── executor.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   └── approval.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── tools/
│   │   ├── rag/
│   │   ├── memory/
│   │   ├── security/
│   │   └── config.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   └── ...
│   ├── package.json
│   └── ...
└── README.md
```

*The structure above is representative; adjust paths to match the current repository.*

## Local Development

### Prerequisites

- Python 3.11
- Node.js and npm
- `uv` (recommended for Python environment management)
- A PostgreSQL database or a local SQLite configuration
- A Google Gemini API key, or a locally running Ollama instance

### 1. Clone the repository

```bash
git clone https://github.com/PiyushKumar74110/HobbyFi-Copilot.git
cd HobbyFi-Copilot
```

### 2. Set up the backend

```bash
cd backend
uv venv
```

Activate the environment in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Create the environment configuration file required by your local setup. For example:

```env
APP_NAME=HobbyFi Copilot
ENVIRONMENT=development
DATABASE_URL=sqlite:///./hobbyfi.db
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
SECRET_KEY=replace_with_a_secure_random_secret
```

For Gemini, configure the provider and API key according to your application settings:

```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.5-flash
```

### 3. Run the backend

From the `backend` directory:

```bash
uv run uvicorn app.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Set up the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

```text
http://localhost:5173
```

Ensure the frontend API base URL points to the backend you are running.

## Deployment

The application is configured for deployment using Render and Neon PostgreSQL.

### Backend

- **Root directory:** `backend`
- **Build command:** `pip install -r requirements.txt`
- **Start command:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Configure production environment variables in the hosting dashboard. Keep database credentials, JWT secrets, and LLM API keys out of source control.

### Frontend

- **Root directory:** `frontend`
- **Build command:** `npm install && npm run build`
- **Publish directory:** `dist`

Set the frontend API base URL to the deployed backend address, and configure backend CORS to allow the deployed frontend origin.

## Engineering Highlights

- Modular separation between API routes, orchestration, execution, tools, and persistence.
- Integration of LLM-driven interactions with structured CRM operations.
- Regression-oriented development and debugging practices.
- Migration from SQLite to PostgreSQL for hosted persistence.
- Support for local and hosted LLM configurations.
- Human approval for supported business-changing workflows.

## Security Considerations

- Keep API keys and database credentials in environment variables.
- Protect all business-data endpoints with authentication.
- Enforce vendor-level authorization in every database query and tool execution path.
- Ensure approval requests are associated with the authenticated vendor and cannot be accessed or modified by other vendors.
- Validate tool inputs and handle errors without exposing sensitive implementation details.

**Note:** Vendor isolation and approval authorization should be verified across all endpoints and tool paths before claiming complete production-grade enforcement.

## Future Improvements

- Expand automated tests for agent planning and tool execution.
- Strengthen authorization and approval-workflow security.
- Add structured LLM evaluation and regression benchmarks.
- Improve observability, audit logging, and error tracing.
- Introduce rate limiting and production monitoring.
- Expand retrieval evaluation and source-grounded response validation.

## Author

**Piyush Kumar**

- GitHub: [PiyushKumar74110](https://github.com/PiyushKumar74110)
