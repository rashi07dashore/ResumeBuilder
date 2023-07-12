from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Cv(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    s_name = models.CharField(max_length=500)
    s_level = models.CharField(max_length=500)


    def __str__(self):
        return self.s_name



class Experince(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    e_office = models.CharField(max_length=500)
    e_position = models.CharField(max_length=500)
    e_duration = models.CharField(max_length=500)

    def __str__(self):
        return self.s_name


class Academic(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    a_institution = models.CharField(max_length=500)
    a_year = models.CharField(max_length=500)
    a_award = models.CharField(max_length=500)

    def __str__(self):
        return self.a_institution



class Referee(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    r_name = models.CharField(max_length=500)
    r_email = models.CharField(max_length=500)
    r_phone = models.CharField(max_length=500)

    def __str__(self):
        return self.r_name



class Profile(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=500)
    mname = models.CharField(max_length=500)
    gender = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    region = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    occupation = models.CharField(max_length=500)
    dob = models.DateField(default='None')
    bio = models.TextField()
    avator = models.ImageField(upload_to='profile/', default='profile/avator.png', null=True)


    def __str__(self):
        return self.fname

    def delete(self, *args, **kwargs):
        self.avator.delete()
        super().delete(*args, **kwargs)




