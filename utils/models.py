from pyexpat import model
from statistics import mode
from django.db import models
from django.core.validators import RegexValidator

class Course(models.Model):
    course_ID = models.CharField(
                            validators=[RegexValidator(regex='^.{4}$', 
                            message='Length has to be 4')],
                            max_length=4)
    courses = (
        (0, "Select Course"),
        (1, "B.Tech"),
        (2, "M.Tech"),
        (3, "MBA")
    )
    course_name = models.IntegerField(choices=courses, default=0)
    course_desc = models.TextField(default="", blank=True)

    def __str__(self) -> str:
        return f"{self.get_course_name_display()} ({self.course_ID})"

class Subjects(models.Model):
    sub_ID = models.CharField(
                            validators=[RegexValidator(regex='^.{4}$', 
                            message='Length has to be 4')],
                            max_length=4,primary_key=True)
    name = models.CharField(max_length=100, default="")
    course_ID = models.ManyToManyField(Course)

    def __str__(self) -> str:
        return f"{self.name} ({self.sub_ID})"