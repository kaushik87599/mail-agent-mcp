📧 MailAgent-MCP: The Agentic Email Assistant

MailAgent-MCP is a local, privacy-first AI Agent designed to triage, organize, and manage Gmail inboxes autonomously.

Unlike standard "AI Assistants" that just summarize text, this project uses the Model Context Protocol (MCP) to give the AI "Hands"—allowing it to draft replies, trash spam, and label threads based on semantic understanding, all securely controlled by the user.

🏗️ Architecture

The system follows a modern 3-Tier Agentic Architecture:

graph LR
    User[User / React UI] <-->|WebSocket| API[FastAPI Backend]
    API <-->|Context & Tools| Brain[LLM (Gemini/Claude)]
    API <-->|MCP Protocol| MCPServer[MCP Server (Python)]
    MCPServer <-->|OAuth 2.0| Gmail[Google Gmail API]


The Brain: An LLM (Large Language Model) reasoning engine.

The Bridge (FastAPI): A high-performance API that orchestrates the conversation and tool execution.

The Hands (MCP Server): A local server implementing the Model Context Protocol to interface with the Gmail API.

The Face (Next.js): A real-time dashboard for chat and live activity logging (Coming Soon).

⚡ Features

✅ Implemented (Logic Layer)

Secure Authentication: OAuth 2.0 integration with Google (No password storage).

Smart Triage: list_unread_emails tool to fetch and display recent threads.

Safety-First Actions:

create_draft: The AI writes the email, but saves it to Drafts for human review.

trash_email: Allows for bulk cleanup of semantic spam (e.g., "Delete all newsletters").

MCP Compliance: Fully compatible with the Model Context Protocol Inspector.

🚧 In Progress (Application Layer)

FastAPI Backend: Connecting the MCP tools to a live WebSocket API.

Next.js Dashboard: A modern UI to chat with the agent and visualize inbox stats.

🛠️ Tech Stack

Core Logic: Python 3.10+, fastmcp, google-api-python-client

Protocol: Model Context Protocol (MCP)

Backend API: FastAPI, Uvicorn, WebSockets

Frontend: Next.js, React, Tailwind CSS

Auth: Google OAuth 2.0

🚀 Getting Started

Prerequisites

Python 3.10 or higher

Node.js & npm (for the Inspector/Frontend)

A Google Cloud Project with Gmail API enabled.

1. Installation

Clone the repository and set up the backend environment:

git clone [https://github.com/yourusername/mail-agent-mcp.git](https://github.com/yourusername/mail-agent-mcp.git)
cd mail-agent-mcp

# Setup Virtual Environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt


(Note: If requirements.txt is missing, install manually: pip install fastmcp google-api-python-client google-auth-oauthlib fastapi uvicorn)

2. Google OAuth Setup (Crucial)

Go to Google Cloud Console.

Create a project and enable the Gmail API.

Configure "OAuth Consent Screen" (External -> Testing -> Add your email as a Test User).

Create OAuth Client ID credentials (Desktop App).

Download the JSON file, rename it to credentials.json, and place it in the backend/ folder.

3. Authenticate

Run the auth script to generate your session token:

python auth.py


Follow the browser prompts to log in. This will generate a token.json file.

4. Run the Agent (Dev Mode)

To test the agent logic using the MCP Inspector web interface:

npx @modelcontextprotocol/inspector python server.py


This will open a local web page where you can manually trigger tools like list_unread_emails to verify the connection.

📂 Project Structure

mail-agent-mcp/
├── backend/
│   ├── auth.py           # OAuth 2.0 Login Handler
│   ├── server.py         # MCP Server & Tool Definitions
│   ├── main.py           # FastAPI Web Server (Upcoming)
│   ├── credentials.json  # (IGNORED) Google App Keys
│   └── token.json        # (IGNORED) User Session Keys
├── frontend/             # Next.js React App (Upcoming)
├── .gitignore            # Security rules
└── README.md             # Documentation


🛡️ Privacy & Safety

Local Execution: The agent runs on your machine. Data is not sent to third-party middleware, only exchanged between your machine, the LLM provider (Google/Anthropic), and Gmail.

Soft Deletes: The agent uses trash (recoverable) instead of delete (permanent).

Draft Mode: The agent creates drafts but cannot hit "Send" automatically.

🤝 Contributing

This is a student project exploring Agentic AI. Issues and Pull Requests are welcome!

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request