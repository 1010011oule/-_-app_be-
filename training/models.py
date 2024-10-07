from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    nickname = models.CharField(max_length=100)
    student_id = models.CharField(max_length=10, unique=True)

# Level Model
class Level(models.Model):
    level_number = models.IntegerField(unique=True)  # Level numbers, e.g., 1, 2, 3, etc.

    def __str__(self):
        return f"Level {self.level_number}"

# Section Model (reading or listening)
class Section(models.Model):
    SECTION_TYPES = (
        ('reading', 'Reading'),
        ('listening', 'Listening'),
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=10, choices=SECTION_TYPES)

    def __str__(self):
        return f"{self.section_type.capitalize()} - Level {self.level.level_number}"

# Exercise Model
class Exercise(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='exercises')
    question_text = models.TextField()  # The question for the exercise
    correct_answer = models.CharField(max_length=1)  # Correct answer, e.g., 'A', 'B', 'C', 'D'
    answer_choices = models.TextField(default="A: , B: , C: , D: ")  # Default value

    def __str__(self):
        return self.question_text


# User Progress Model
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user.nickname} - {self.exercise.question_text} - {'Correct' if self.is_correct else 'Incorrect'}"

