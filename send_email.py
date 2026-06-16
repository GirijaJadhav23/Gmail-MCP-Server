import base64
from typing import Optional
from email.mime.text import MIMEText

from auth import get_gmail_service


def send_email(
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
):
    """
    Send email.

    Args:
        to: Recipient email address (comma-separated for multiple).
        subject: Email subject line.
        body: Email body text.
        cc: CC recipients (comma-separated for multiple).
        bcc: BCC recipients (comma-separated for multiple).
    """
    service = get_gmail_service()

    mime_message = MIMEText(body)
    mime_message["to"] = to
    mime_message["subject"] = subject

    if cc:
        mime_message["cc"] = cc
    if bcc:
        mime_message["bcc"] = bcc

    raw_message = base64.urlsafe_b64encode(
        mime_message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={"raw": raw_message},
    ).execute()

    return {"message_id": result["id"]}
