from typing import Optional

from auth import get_gmail_service


def search_emails(
    query: str,
    max_results: int = 10,
    from_address: Optional[str] = None,
    to_address: Optional[str] = None,
    subject: Optional[str] = None,
    after_date: Optional[str] = None,
    before_date: Optional[str] = None,
    has_attachment: bool = False,
    label: Optional[str] = None,
):
    """
    Search emails using Gmail search syntax.

    Args:
        query: Free-text search query (same as Gmail search box).
        max_results: Maximum number of results to return.
        from_address: Filter by sender email address.
        to_address: Filter by recipient email address.
        subject: Filter by subject line.
        after_date: Only emails after this date (format: YYYY/MM/DD).
        before_date: Only emails before this date (format: YYYY/MM/DD).
        has_attachment: If True, only return emails with attachments.
        label: Filter by Gmail label (e.g. "INBOX", "STARRED").
    """
    # Build Gmail search query
    parts = [query] if query else []

    if from_address:
        parts.append(f"from:{from_address}")
    if to_address:
        parts.append(f"to:{to_address}")
    if subject:
        parts.append(f"subject:{subject}")
    if after_date:
        parts.append(f"after:{after_date}")
    if before_date:
        parts.append(f"before:{before_date}")
    if has_attachment:
        parts.append("has:attachment")
    if label:
        parts.append(f"label:{label}")

    search_query = " ".join(parts)

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q=search_query,
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return {"query": search_query, "count": 0, "emails": []}

    output = []

    for msg in messages:
        message = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["Subject", "From", "Date"],
        ).execute()

        headers = message.get("payload", {}).get("headers", [])

        header_map = {h["name"]: h["value"] for h in headers}

        output.append({
            "id": msg["id"],
            "subject": header_map.get("Subject", "No Subject"),
            "from": header_map.get("From", "Unknown"),
            "date": header_map.get("Date", "Unknown"),
            "snippet": message.get("snippet", ""),
        })

    return {
        "query": search_query,
        "count": len(output),
        "emails": output,
    }
