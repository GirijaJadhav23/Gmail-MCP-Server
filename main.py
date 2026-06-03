from mcp.server.fastmcp import FastMCP

from tools.list_emails import list_emails
from tools.read_email import read_email
from tools.send_email import send_email
from tools.search_emails import search_emails
from tools.send_email_with_attachment import send_email_with_attachment
from tools.count_emails_from import count_emails_from
from tools.detect_priority_emails import detect_priority_emails
from tools.create_draft import create_draft
from tools.delete_email import delete_email
from tools.mark_as_read import mark_as_read
from tools.mark_as_unread import mark_as_unread
from tools.archive_email import archive_email

mcp = FastMCP("gmail-server")

# Register tools
mcp.tool()(list_emails)
mcp.tool()(read_email)
mcp.tool()(send_email)
mcp.tool()(search_emails)
mcp.tool()(send_email_with_attachment)
mcp.tool()(count_emails_from)
mcp.tool()(detect_priority_emails)
mcp.tool()(create_draft)
mcp.tool()(delete_email)
mcp.tool()(mark_as_read)
mcp.tool()(mark_as_unread)
mcp.tool()(archive_email)

if __name__ == "__main__":
    mcp.run()
