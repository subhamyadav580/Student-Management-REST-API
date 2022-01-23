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
