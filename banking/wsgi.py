"""
WSGI config for banking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from django.contrib.auth import get_user_model #remove later

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking.settings')

application = get_wsgi_application()


#Remove below later
if os.environ.get('RUN_MAIN') != 'true':  # Prevents double-run on reload
    from django.core.management import call_command
    try:
        call_command('migrate')
        call_command('collectstatic', interactive=False, verbosity=0)
    except Exception as e:
        print("Startup error:", e)
