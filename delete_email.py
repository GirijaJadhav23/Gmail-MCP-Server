from auth import get_gmail_service


def delete_email(message_id: str, permanent: bool = False):
    """
    Delete an email. By default moves to Trash. Set permanent=True to permanently delete.

    Args:
        message_id: The ID of the email to delete.
        permanent: If True, permanently deletes (cannot be recovered). Default is False (moves to Trash).
    """
    service = get_gmail_service()

    if permanent:
        service.users().messages().delete(
            userId="me",
            id=message_id,
        ).execute()
        return {
            "message_id": message_id,
            "status": "Permanently deleted",
        }
    else:
        service.users().messages().trash(
            userId="me",
            id=message_id,
        ).execute()
        return {
            "message_id": message_id,
            "status": "Moved to Trash",
        }
