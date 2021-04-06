import smtplib
from django.core.mail import send_mail
from accounts.user_types import UserTypes

class MailSender:
    @staticmethod
    def send_mail(title, message, recipient):
        try:
            # Use default from email.
            send_mail(subject=title, message="", from_email=None, recipient_list=[recipient], fail_silently=False, html_message=message)
            return True
        except smtplib.SMTPException as ex:
            print(f"Failure sending email: {ex}")
    
        return False

    @staticmethod
    def create_send_registration_link_title(user):
        return f"Admin {user.profile.public_name} has invited you to create an account in WMRC!"
    
    @staticmethod
    def create_send_registration_link_message(link, url_path):
        acc_type_prep = f"a <b>User</b>" if link.type == UserTypes.user else f"an <b>Admin</b>"

        return f"Hello. <br>" \
            + f"You have been invited to create {acc_type_prep} account in the Wall Mounted Room Calendar system.<br>" \
            + "Please follow the link below to register:<br>" \
            + f"{url_path}" \
            + "<br><br>" \
            + f"<span style='color:red'> <b>The link is valid until {link.valid_until.strftime('%d.%m.%Y %H:%M')}!!! </b> </span>" \
            + "<br><br>" \
            + MailSender.message_signature()

    @staticmethod
    def message_signature():
        return "Best regards,<br>" \
                + "The WMRC team"   
