from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command

class Command(BaseCommand):
    help = "Runs initial migration and creates default superuser"

    def handle(self, *args, **kwargs):
        call_command('migrate')

        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpass123'
            )
            self.stdout.write(self.style.SUCCESS("Superuser created."))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))
