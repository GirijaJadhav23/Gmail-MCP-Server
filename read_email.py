from auth import get_gmail_service


def read_email(message_id: str):
    """
    Read a Gmail message.
    """
    service = get_gmail_service()

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    return message
