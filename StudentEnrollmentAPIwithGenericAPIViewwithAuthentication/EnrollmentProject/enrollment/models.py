from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    email = models.EmailField(unique=True)
    age = models.IntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.name