from auth import get_gmail_service


def detect_priority_emails(max_results: int = 10):
    """
    Detect priority/important emails from inbox.
    Returns unread emails marked as important or from frequent senders.

    Args:
        max_results: Maximum number of priority emails to return.
    """
    service = get_gmail_service()

    # Search for unread important emails
    results = service.users().messages().list(
        userId="me",
        q="is:unread is:important",
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return {"count": 0, "priority_emails": []}

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

        labels = message.get("labelIds", [])

        output.append({
            "id": msg["id"],
            "subject": header_map.get("Subject", "No Subject"),
            "from": header_map.get("From", "Unknown"),
            "date": header_map.get("Date", "Unknown"),
            "snippet": message.get("snippet", ""),
            "labels": labels,
        })

    return {
        "count": len(output),
        "priority_emails": output,
    }
