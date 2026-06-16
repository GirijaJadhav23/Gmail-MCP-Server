from auth import get_gmail_service


def count_emails_from(email_address: str):
    """
    Return the count of emails received from a specific sender.

    Args:
        email_address: The sender's email address or name to count emails from.
    """
    service = get_gmail_service()

    # Use Gmail search to find all emails from this sender
    query = f"from:{email_address}"

    # First call to get estimate
    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=500,
    ).execute()

    messages = results.get("messages", [])
    total = len(messages)

    # Handle pagination if more than 500
    while "nextPageToken" in results:
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=500,
            pageToken=results["nextPageToken"],
        ).execute()
        messages = results.get("messages", [])
        total += len(messages)

    return {
        "email_address": email_address,
        "count": total,
    }
