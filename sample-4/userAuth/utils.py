from django.core.mail import EmailMessage

class Util:
    def send_mail(data):
        """send_mail() function sends registration verification mail and password reset mail"""
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']],)
        print("email ",email)
        email.send()
