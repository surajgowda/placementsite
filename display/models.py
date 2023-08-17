from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    # DEPARTMENT_CHOICES = [
    #     ('IT', 'Information Technology'),
    #     ('MCA', 'Master of Computer Applications'),
    #     ('ISE', 'Information Science and Engineering'),
    #     ('ECE', 'Electronics and Communication Engineering'),
    #     ('EEE', 'Electrical and Electronics Engineering'),
    #     ('CSE', 'Computer Science and Engineering'),
    #     ('ME', 'Mechanical Engineering'),
    #     ('CE', 'Civil Engineering'),
    #     ('Mtech', 'Master of Technology'),
    #     # Add more choices as needed
    # ]
    # department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.name
    
class Updates(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.company.name + " -- " + self.title


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(_("Age"), null=True, blank=True)
    passout_year = models.PositiveIntegerField(_("Passout Year"), null=True, blank=True)
    department = models.TextField(_("Department"), null=True, blank=True)
    companies_applied = models.ManyToManyField(Company)    
    
    # Add any other additional fields or methods as needed

    def __str__(self):
        return self.username    
    
    
class Notifications(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="Please check your email for more information")
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title