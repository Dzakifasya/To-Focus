import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_app.settings")

from django.core.management import execute_from_command_line

execute_from_command_line([
    "manage.py",
    "runserver",
    "127.0.0.1:8000",
    "--noreload"
])
