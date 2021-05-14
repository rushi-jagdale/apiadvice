from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CreateUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.user

class Advisor(models.Model):
   
    advisor_name = models.CharField(max_length=20)
    advisor_image=models.ImageField(upload_to='addimages')
   
    def __str__(self):
        return str(self.advisor_name)

        