import traceback

import pyotp
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from e_commerce.models import OTPRecord


class OTPManager:
    @staticmethod
    def generate_and_send_otp(email, user_name):
        """
        Generate OTP and send email

        Returns:
        tuple: (success, message)
        """
        try:
            # Create or update OTP record
            otp_record = OTPRecord.create_otp_record(email)
            otp_code = otp_record.get_otp()

            context = {
                'user_name': user_name,
                'otp_code': otp_code,
            }

            # Render email templates
            html_message = render_to_string('emails/otp_email.html', context)

            plain_message = strip_tags(html_message)

            # Send email
            send_mail(
                subject='Trade Streak-Your Verification Code',
                message=plain_message,
                from_email='support@tradestreakai.com',
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            # print(otp_code)
            return True, "OTP sent successfully"

        except Exception as e:
            return False, str(e)

    @staticmethod
    def verify_otp(email, otp_input):
        """
        Verify provided OTP

        Returns:
        tuple: (success, message)
        """
        try:
            # Get OTP record for email
            otp_record = OTPRecord.objects.get(email=email)

            if not otp_record.is_valid():
                return False, "OTP has expired"

            totp = pyotp.TOTP(otp_record.otp_secret, interval=600)
            print(totp, otp_record.otp_secret)
            # Verify OTP
            if totp.verify(str(otp_input)):
                otp_record.is_verified = True
                otp_record.save()
                return True, "OTP verified Successfully"

            return False, "Invalid OTP"

        except OTPRecord.DoesNotExist:

            return False, "No valid OTP found"
        except Exception as e:
            traceback.print_exc()
            return False, "Error verifying OTP"