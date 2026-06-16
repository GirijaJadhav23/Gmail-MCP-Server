import base64
import mimetypes
import os
from typing import Optional
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

from auth import get_gmail_service


def send_email_with_attachment(
    to: str,
    subject: str,
    body: str,
    attachment_path: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
):
    """
    Send an email with a file attachment.

    Args:
        to: Recipient email address (comma-separated for multiple).
        subject: Email subject line.
        body: Email body text.
        attachment_path: Absolute path to the file to attach.
        cc: CC recipients (comma-separated for multiple).
        bcc: BCC recipients (comma-separated for multiple).
    """
    # Validate attachment exists
    if not os.path.isfile(attachment_path):
        return {"error": f"File not found: {attachment_path}"}

    # Check file size (Gmail limit is 25MB)
    file_size = os.path.getsize(attachment_path)
    max_size = 25 * 1024 * 1024  # 25MB

    if file_size > max_size:
        return {
            "error": f"File too large: {file_size / (1024*1024):.1f}MB. Gmail limit is 25MB."
        }

    service = get_gmail_service()

    # Create multipart message
    mime_message = MIMEMultipart()
    mime_message["to"] = to
    mime_message["subject"] = subject

    if cc:
        mime_message["cc"] = cc
    if bcc:
        mime_message["bcc"] = bcc

    # Attach body text
    mime_message.attach(MIMEText(body, "plain"))

    # Detect MIME type of attachment
    content_type, _ = mimetypes.guess_type(attachment_path)
    if content_type is None:
        content_type = "application/octet-stream"

    main_type, sub_type = content_type.split("/", 1)

    # Read and attach the file
    with open(attachment_path, "rb") as f:
        attachment = MIMEBase(main_type, sub_type)
        attachment.set_payload(f.read())

    encoders.encode_base64(attachment)

    filename = os.path.basename(attachment_path)
    attachment.add_header(
        "Content-Disposition", "attachment", filename=filename
    )

    mime_message.attach(attachment)

    # Encode and send
    raw_message = base64.urlsafe_b64encode(
        mime_message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={"raw": raw_message},
    ).execute()

    return {
        "message_id": result["id"],
        "attachment": filename,
        "attachment_size_kb": round(file_size / 1024, 1),
    }
