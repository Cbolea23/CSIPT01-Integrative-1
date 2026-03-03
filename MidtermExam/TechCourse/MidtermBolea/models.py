from django.db import models

# Create your models here.
class Professor(models.Model):
    ProfessorID = models.CharField(max_length=20, primary_key=True)
    Name = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)

    def __str__(self):
        return self.Name
    
class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    CourseCode = models.CharField(max_length=20, unique=True)
    CourseName = models.CharField(max_length=100)
    Credits = models.IntegerField()
    Amount_per_Credits = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.CourseCode

class Assignment(models.Model):
    assignment_id = models.CharField(max_length=20, primary_key=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    Total_Amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title
    