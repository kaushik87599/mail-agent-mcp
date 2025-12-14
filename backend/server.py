from fastmcp import FastMCP
import os.path
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize
mcp = FastMCP("Gmail Agent")

def get_gmail_service():
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
        return build("gmail", "v1", credentials=creds)
    else:
        raise ValueError("Authentication required.No token.json found. Run auth.py first.")

# --- TOOL 1: List (Updated with ID) ---
@mcp.tool()
def list_unread_emails(limit: int = 5) -> str:
    """List unread emails with their IDs. Always use this first to get IDs."""
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", q="is:unread", maxResults=limit).execute()
    messages = results.get("messages", [])

    if not messages:
        return "No unread messages found."

    output = []
    for msg in messages:
        msg_id = msg['id'] # Grab the ID
        full_msg = service.users().messages().get(userId="me", id=msg_id).execute()
        headers = full_msg["payload"]["headers"]
        
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown)")
        
        # We format it so the AI (and you) can easily copy the ID
        output.append(f"🆔 ID: {msg_id}\n📧 From: {sender}\n📄 Subject: {subject}\n-------------------")

    return "\n".join(output)

# --- TOOL 2: Create Draft (Safe Reply) ---
@mcp.tool()
def create_draft(to_email: str, subject: str, body_text: str) -> str:
    """Creates a draft email. formatting is plain text."""
    service = get_gmail_service()
    
    try:
        message = EmailMessage()
        message.set_content(body_text)
        message["To"] = to_email
        message["Subject"] = subject

        # Encode the message for Gmail API
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}

        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        return f"✅ Draft created successfully! Draft ID: {draft['id']}"
    
    except HttpError as error:
        return f"❌ An error occurred: {error}"

# --- TOOL 3: Trash Email (Cleanup) ---
@mcp.tool()
def trash_email(message_id: str) -> str:
    """Moves an email to Trash. (Reversible for 30 days)."""
    service = get_gmail_service()
    try:
        service.users().messages().trash(userId="me", id=message_id).execute()
        return f"🗑️ Moved message {message_id} to Trash."
    except HttpError as error:
        return f"❌ Failed to trash email: {error}"

if __name__ == "__main__":
    mcp.run()