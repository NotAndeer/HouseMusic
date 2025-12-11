"""Email service for transactional and campaign emails."""

import logging
from typing import List, Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

from app.core.config import settings


logger = logging.getLogger(__name__)


class EmailService:
    """Service to send emails via SMTP (configurable for SendGrid, Gmail, etc.)."""

    def __init__(self) -> None:
        # SMTP configuration from settings
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email

    def send_email(
        self,
        to: str | List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """Send an email to one or more recipients.
        
        Args:
            to: Recipient email address (or list).
            subject: Email subject.
            body: Plain text body.
            html_body: Optional HTML body.
            attachments: List of dicts with keys: 'filename', 'content' (bytes).
        
        Returns:
            True if email was sent successfully, False otherwise.
        """
        if isinstance(to, str):
            to = [to]

        msg = MIMEMultipart("alternative")
        msg["From"] = self.from_email
        msg["To"] = ", ".join(to)
        msg["Subject"] = subject

        # Add plain text part
        msg.attach(MIMEText(body, "plain"))

        # Add HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html"))

        # Add attachments
        if attachments:
            for attachment in attachments:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment["content"])
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{attachment["filename"]}"'
                )
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_port in (465,):
                    # SSL connection
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                elif self.smtp_port in (587,):
                    # TLS connection
                    server.starttls()

                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)

                server.sendmail(self.from_email, to, msg.as_string())
                logger.info("Email sent to %s: %s", to, subject)
                return True

        except Exception as e:
            logger.error("Failed to send email to %s: %s", to, e)
            return False


def get_email_service() -> EmailService:
    """Dependency helper for routers and services."""
    return EmailService()