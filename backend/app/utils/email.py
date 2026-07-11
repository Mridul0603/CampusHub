import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
import logging

logger = logging.getLogger(__name__)


def send_password_reset_email(to_email: str, reset_token: str, full_name: str) -> None:
    """
    Send a password reset email with the raw token embedded in a link.
    In production, swap this with SendGrid, Resend, or SES.
    """
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    html_body = f"""
    <html><body>
      <h2>Password Reset — CampusHub</h2>
      <p>Hi {full_name},</p>
      <p>We received a request to reset your password.</p>
      <p>
        <a href="{reset_url}" style="
          background:#4F46E5; color:white; padding:12px 24px;
          border-radius:6px; text-decoration:none; font-weight:600;
        ">Reset My Password</a>
      </p>
      <p>This link expires in 30 minutes. If you didn't request this, ignore this email.</p>
      <p>— The CampusHub Team</p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset your CampusHub password"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
        logger.info(f"Password reset email sent to {to_email}")
    except Exception as e:
        # Don't crash the request if email fails; log and continue
        logger.error(f"Failed to send reset email to {to_email}: {e}")
