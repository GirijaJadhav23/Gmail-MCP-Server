from auth import get_gmail_service


def archive_email(message_id: str):
    """
    Archive an email (remove from inbox but keep in account).

    Args:
        message_id: The ID of the email to archive.
    """
    service = get_gmail_service()

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["INBOX"]},
    ).execute()

    return {"message_id": message_id, "status": "archived"}
