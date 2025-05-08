import os
import sys
import django
from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_project.settings")
    
    # Initialize Django before loading the ASGI application
    django.setup()
    
    sys.argv = ["daphne", "chat_project.asgi:application"]
    CommandLineInterface.entrypoint()