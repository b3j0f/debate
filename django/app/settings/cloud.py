# -*- coding: utf-8 -*-
"""Cloud settings."""

from .base import *
import os


DEBUG = False

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Set the email backend to a dummy backend since we cannot send email from this application
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
