from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from pigeon.notification import Notification


def send_emails(notification):
    messages = []
    context = {'site': notification.site}
    for user in notification.users:
        message = render_to_string(notification.template_name, context)
        messages.append([
            notification.subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        ])
    send_mass_mail(messages)


class DeletionNotification(Notification):
    handlers = (send_emails,)
    template_name = 'user_deletion/email_notification.txt'
    subject = _('Re-activate your account')


class DeletedNotification(Notification):
    handlers = (send_emails,)
    template_name = 'user_deletion/email_deletion.txt'
    subject = _('Your account has been deleted')
