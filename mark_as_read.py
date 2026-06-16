from auth import get_gmail_service


def mark_as_read(message_id: str):
    """
    Mark an email as read.

    Args:
        message_id: The ID of the email to mark as read.
    """
    service = get_gmail_service()

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()

    return {"message_id": message_id, "status": "read"}
