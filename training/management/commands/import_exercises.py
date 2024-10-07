import csv
from django.core.management.base import BaseCommand
from training.models import Section, Exercise

class Command(BaseCommand):
    help = 'Imports exercises from a CSV file'

    def handle(self, *args, **kwargs):
        # Path to the CSV file
        csv_file_path = 'data/exercises.csv'

        # Open and read the CSV file
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row if it exists

            # Iterate over rows in the CSV and insert into Exercise model
            for row in reader:
                # Skip empty rows
                if not row or len(row) < 4:
                    continue

                section_id, question_text, answer_choices, correct_answer = row
                section = Section.objects.get(id=section_id)
                
                # Create the exercise object
                Exercise.objects.create(
                    section=section,
                    question_text=question_text,
                    answer_choices=answer_choices,
                    correct_answer=correct_answer
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported exercises'))

