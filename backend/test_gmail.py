import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def test_connection():
    # Load credentials
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    # Connect to Gmail API
    service = build("gmail", "v1", credentials=creds)

    # 1. Get Profile Info
    profile = service.users().getProfile(userId="me").execute()
    email_address = profile.get("emailAddress")
    total_messages = profile.get("messagesTotal")

    print(f"✅ SUCCESS!")
    print(f"Connected to: {email_address}")
    print(f"Total Emails: {total_messages}")

    # 2. List last 3 emails (Subject lines only)
    print("\n--- Last 3 Emails ---")
    results = service.users().messages().list(userId="me", maxResults=6).execute()
    messages = results.get("messages", [])

    for msg in messages:
        # We need to fetch the specific email details to get the Subject
        full_msg = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = full_msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        print(f"- {subject}")

if __name__ == "__main__":
    test_connection()