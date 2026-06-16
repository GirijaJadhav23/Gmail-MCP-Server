from auth import get_gmail_service


def mark_as_unread(message_id: str):
    """
    Mark an email as unread.

    Args:
        message_id: The ID of the email to mark as unread.
    """
    service = get_gmail_service()

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"addLabelIds": ["UNREAD"]},
    ).execute()

    return {"message_id": message_id, "status": "unread"}
