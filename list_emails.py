from auth import get_gmail_service


def list_emails(max_results: int = 10):
    """
    List recent emails.
    """
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    output = []

    for msg in messages:
        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"),
            "No Subject"
        )

        output.append({
            "id": msg["id"],
            "subject": subject
        })

    return output
