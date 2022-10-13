from django.db import models

# Create your models here.

class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=10)
    experience = models.CharField(max_length=20)
    interest = models.CharField(max_length=50)
    resume = models.FileField(upload_to="resume/pdfs/")
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=10, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name
    