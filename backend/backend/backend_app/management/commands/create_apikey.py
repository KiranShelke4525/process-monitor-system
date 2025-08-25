from django.core.management.base import BaseCommand
from backend_app.models import ApiKey
import secrets

class Command(BaseCommand):
    help = "Create a new API key"

    def add_arguments(self, parser):
        parser.add_argument('--name', default='agent')

    def handle(self, *args, **options):
        key = secrets.token_hex(32)
        ApiKey.objects.create(name=options['name'], key=key)
        self.stdout.write(self.style.SUCCESS(key))
