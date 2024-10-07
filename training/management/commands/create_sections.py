from django.core.management.base import BaseCommand
from training.models import Level, Section

class Command(BaseCommand):
    help = 'Create reading and listening sections for all levels'

    def handle(self, *args, **kwargs):
        for level_number in range(1, 7):  # Levels 1 to 6
            level, created = Level.objects.get_or_create(level_number=level_number)
            Section.objects.get_or_create(level=level, section_type='reading')
            Section.objects.get_or_create(level=level, section_type='listening')

        self.stdout.write(self.style.SUCCESS('Successfully created sections for levels 1-6'))

