import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.core.config import settings

class EmailService:
    @staticmethod
    def send_reset_password_email(to_email: str, new_password: str) -> bool:
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD or settings.SMTP_PASSWORD == "PASTE_YOUR_16_CHAR_APP_PASSWORD_HERE":
            print(f"[EMAIL] Skipping email to {to_email}. SMTP credentials not configured yet.")
            print(f"[EMAIL] Please update SMTP_PASSWORD in your .env file with a Gmail App Password.")
            return False

        message = MIMEMultipart()
        message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = "Password Reset - NECO Data Portal"

        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
                    <h2 style="color: #2e7d32;">NECO Data Portal</h2>
                    <p>Hello,</p>
                    <p>Your password has been reset by the administrator. Please use the temporary password below to log in:</p>
                    <div style="background-color: #f1f8e9; padding: 15px; border-radius: 4px; font-size: 20px; font-weight: bold; text-align: center; color: #2e7d32; letter-spacing: 2px;">
                        {new_password}
                    </div>
                    <p>For security reasons, we recommend changing this password immediately after logging in.</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 12px; color: #777;">This is an automated message from NECO Data Portal. Please do not reply.</p>
                </div>
            </body>
        </html>
        """
        message.attach(MIMEText(body, "html"))

        try:
            print(f"[EMAIL] Sending password reset email to {to_email} via {settings.SMTP_HOST}...")
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(message)
            print(f"[EMAIL] Successfully sent to {to_email}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"[EMAIL] Authentication failed! Your Gmail App Password is incorrect or expired.")
            print(f"[EMAIL] Go to https://myaccount.google.com/apppasswords to generate a new one.")
            print(f"[EMAIL] Error: {e}")
            return False
        except Exception as e:
            print(f"[EMAIL] Failed to send email to {to_email}: {e}")
            return False
