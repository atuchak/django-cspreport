import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csp_report.tests.test_settings')


def pytest_configure():
    settings.DEBUG = False
    django.setup()