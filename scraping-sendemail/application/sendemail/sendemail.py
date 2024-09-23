import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    @classmethod
    def send_email(
        cls,
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        subject: str,
        message: str,
    ):
        if not sender_email:
            raise ValueError("sender_email is empty")
        if not sender_password:
            raise ValueError("sender_password is empty")

        mimeobj = MIMEMultipart()
        mimeobj["From"] = sender_email
        mimeobj["To"] = recipient_email
        mimeobj["Subject"] = subject

        text = MIMEText(message, "plain", "utf-8")
        mimeobj.attach(text)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, recipient_email, mimeobj.as_string())
