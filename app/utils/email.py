from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings


async def send_verification_email(email: str, code: str):
	msg = EmailMessage()
	msg["From"] = settings.SMTP_USERNAME
	msg["To"] = email
	msg["Subject"] = "Email Verification Code"
	msg.set_content(f"Your verification code: {code}")

	await aiosmtplib.send(msg, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT,
	                      username=settings.SMTP_USERNAME, password=settings.SMTP_PASSWORD, use_tls=False)
