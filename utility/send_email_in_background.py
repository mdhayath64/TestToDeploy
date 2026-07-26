from datetime import datetime

from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import threading


class EmailThread(threading.Thread):
    """
    Separate thread for sending emails asynchronously
    """

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class EmailSender:
    @staticmethod
    def send_email(subject, to_email, template_name, context, attachments=None):
        """
        Send HTML email with optional attachments

        Args:
            subject (str): Email subject
            to_email (str or list): Recipient email(s)
            template_name (str): Path to HTML email template
            context (dict): Context data for email template
            attachments (list): Optional list of attachment tuples (filename, content, mimetype)
        """
        try:
            # Render HTML content
            html_content = render_to_string(template_name, context)
            text_content = strip_tags(html_content)  # Create plain text version

            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email] if isinstance(to_email, str) else to_email
            )

            # Attach HTML version
            email.attach_alternative(html_content, "text/html")

            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    email.attach(*attachment)

            # Send email in background
            EmailThread(email).start()

            return True, "Email sent successfully"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def send_simple_email(subject, message, to_email):
        """
        Send simple text email without HTML template

        Args:
            subject (str): Email subject
            message (str): Email body text
            to_email (str or list): Recipient email(s)
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email] if isinstance(to_email, str) else to_email
            )

            EmailThread(email).start()

            return True, "Email sent successfully"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def send_otp_email(email, user_name, otp_code):
        """
        Send OTP email to user

        Args:
            email (str): Recipient email address
            user_name (str): Name of the recipient
        """

        # Email context
        context = {
            'user_name': user_name,
            'otp_code': otp_code,
        }

        # Render email templates
        html_message = render_to_string('emails/otp_email.html', context)
        plain_message = strip_tags(html_message)

        # Send email
        try:
            send_mail(
                subject='TradeStreak-Your Verification Code',
                message=plain_message,
                from_email='support@tradestreakai.com',
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            return True, otp_code
        except Exception as e:
            return False, str(e)
