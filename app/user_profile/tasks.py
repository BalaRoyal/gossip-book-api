from django.conf import settings
import threading
from threading import Thread
from django.core.mail.message import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content,
                           settings.EMAIL_HOST_USER, self.recipient_list)

        msg.content_subtype = "html"
        msg.send()


def send_email(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()
