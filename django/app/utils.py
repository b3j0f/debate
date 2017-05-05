# coding: utf-8
"""Model module."""
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives


def sendemail(subject, msg, html, *to):
    """Send an email."""
    msg = EmailMultiAlternatives(subject, msg, '', to)
    msg.attach_alternative(html, "text/html")
    msg.send()
