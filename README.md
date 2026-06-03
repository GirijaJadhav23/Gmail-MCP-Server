# 📧 Gmail MCP Server

A full-featured Gmail MCP (Model Context Protocol) server that enables AI assistants to read, search, send, and manage emails through natural language.

Built with [FastMCP](https://github.com/jlowin/fastmcp) and the Gmail API.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| `list_emails` | List recent emails from inbox |
| `read_email` | Read full email content by ID |
| `send_email` | Send emails with CC/BCC support |
| `send_email_with_attachment` | Send emails with file attachments (up to 25MB) |
| `search_emails` | Advanced search with filters (sender, date, labels, attachments) |
| `count_emails_from` | Count total emails from a specific sender |
| `detect_priority_emails` | Find unread important/priority emails |
| `create_draft` | Create email drafts without sending |
| `delete_email` | Move to trash or permanently delete |
| `mark_as_read` | Mark an email as read |
| `mark_as_unread` | Mark an email as unread |
| `archive_email` | Archive email (remove from inbox, keep in account) |

---

## 🏗️ Project Structure

```
GmailMcp/
├── main.py                  # MCP server entry point
├── config.py                # Configuration constants (scopes, file paths)
├── auth.py                  # Google OAuth2 authentication logic
├── tools/
│   ├── __init__.py          # Tool registry
│   ├── list_emails.py
│   ├── read_email.py
│   ├── send_email.py
│   ├── send_email_with_attachment.py
│   ├── search_emails.py
│   ├── count_emails_from.py
│   ├── detect_priority_emails.py
│   ├── create_draft.py
│   ├── delete_email.py
│   ├── mark_as_read.py
│   ├── mark_as_unread.py
│   └── archive_email.py
├── credentials.json         # Google OAuth client credentials (not committed)
├── token.json               # Generated OAuth token (not committed)
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## 🔐 OAuth2 Setup (Google Cloud Console)

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Name it (e.g., "Gmail MCP Server") and click **Create**

### Step 2: Enable the Gmail API

1. Navigate to **APIs & Services** → **Library**
2. Search for **"Gmail API"**
3. Click **Enable**

### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (or Internal if using Google Workspace)
3. Fill in the required fields:
   - App name: `Gmail MCP Server`
   - User support email: your email
   - Developer contact: your email
4. Click **Save and Continue**
5. On the **Scopes** page, click **Add or Remove Scopes**
6. Add: `https://www.googleapis.com/auth/gmail.modify`
7. Click **Save and Continue**
8. On **Test users**, add your Gmail address
9. Click **Save and Continue** → **Back to Dashboard**

### Step 4: Create OAuth Client Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `Gmail MCP Desktop Client`
5. Click **Create**
6. Click **Download JSON**
7. Rename the downloaded file to `credentials.json`
8. Place it in the project root directory

### Step 5: Generate Token (First-Time Auth)

Run the server once manually to trigger the browser-based OAuth flow:

```bash
uv run python main.py
```

Or trigger any tool call — the first request will:
1. Open your default browser
2. Ask you to sign in to your Google account
3. Grant the app permission to access Gmail
4. Redirect back and save the token to `token.json`

After this, the server runs without browser interaction (tokens refresh automatically).

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- A Google Cloud project with Gmail API enabled
- `credentials.json` from OAuth setup above

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/GmailMcp.git
cd GmailMcp

# Install dependencies
uv sync
```

### Run the Server

```bash
# Start the MCP server (stdio transport)
uv run python main.py
```

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python main.py
```

This opens a web UI at `http://localhost:6274` where you can interactively test all tools.

---

## ⚙️ Configuration for AI Clients

### Kiro / VS Code MCP Config

Add this to your MCP settings (`mcp.json`):

```json
{
  "mcpServers": {
    "GmailMcp": {
      "command": "uv",
      "args": ["run", "--link-mode=copy", "python", "main.py"],
      "cwd": "/path/to/GmailMcp"
    }
  }
}
```

### Claude Desktop Config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/GmailMcp"
    }
  }
}
```

---

## 📖 Usage Examples

Once connected, you can ask your AI assistant:

- *"List my last 5 emails"*
- *"Search for emails from amazon.com with attachments"*
- *"Send an email to john@example.com with subject 'Meeting' and body 'See you at 3pm'"*
- *"How many emails have I received from notifications@github.com?"*
- *"Show me my priority unread emails"*
- *"Create a draft to boss@company.com about the quarterly report"*
- *"Archive email 19e8b700b6659c7b"*
- *"Mark that email as read"*

---

## 🔒 Security Notes

- `credentials.json` and `token.json` are in `.gitignore` — never commit them
- The OAuth scope (`gmail.modify`) allows reading and sending but **not** permanent deletion by default
- Permanent deletion requires explicit `permanent=True` flag
- Tokens auto-refresh without browser interaction after initial setup

---

## 🛠️ Adding New Tools

1. Create a new file in `tools/` (e.g., `tools/my_new_tool.py`)
2. Import `get_gmail_service` from `auth`
3. Define your function with a docstring (used as tool description)
4. Add the import to `tools/__init__.py`
5. Register it in `main.py` with `mcp.tool()(my_new_tool)`

