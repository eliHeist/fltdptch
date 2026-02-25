from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Setup user groups (roles): Normal User, Supervisor, and Admin'

    def handle(self, *args, **options):
        groups_info = {
            'Normal User': 'A regular user with basic access',
            'Supervisor': 'Can supervise flights and manage aircraft',
            'Admin': 'Full administrative access',
        }

        for group_name, description in groups_info.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Group already exists: {group_name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\nGroups setup complete!')
        )
        self.stdout.write(
            self.style.WARNING('\nNote: Assign users to groups through Django admin or programmatically.')
        )
