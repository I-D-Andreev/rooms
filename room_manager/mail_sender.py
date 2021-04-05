import smtplib
from django.core.mail import send_mail

class MailSender:
    @staticmethod
    def send_mail(title, message, recipient):
        try:
            # Use default from email.
            send_mail(subject=title, message=message, from_email=None, recipient_list=[recipient], fail_silently=False)
            return True
        except smtplib.SMTPException as ex:
            print(f"Failure sending email: {ex}")
    
        return False
