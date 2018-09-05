from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description=models.TextField()
    address=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.PROTECT)
    name=models.CharField(max_length=100,unique=True)
    price=models.IntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class UserProfileInfo(models.Model):
    # create relationship from this class to User
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    # add any more attribute you want
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length = 100)
    portfolio = models.URLField(blank=True)
    picture = models.ImageField(upload_to = "images/",blank=True)

    def __str__(self):
        return self.user.username

    class Meta():
        db_table = "usrprofileinfo"