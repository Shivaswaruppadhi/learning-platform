from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Profile(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField()
    profile_pic = models.ImageField()

    def __str__(self) -> str:
        return str(self.username)
    
class Course(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    prize = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    username = models.CharField(max_length=50)
    title = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.username 