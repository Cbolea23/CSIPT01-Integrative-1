from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    course = models.CharField(max_length=10)
    year_level = models.CharField(max_length=12)
    email = models.EmailField(unique=True)
    is_enrolled = models.BooleanField(default=True)
     
    def __str__(self):
        return self.name