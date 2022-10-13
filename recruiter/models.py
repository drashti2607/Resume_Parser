from django.db import models

# Create your models here.

class selectedResume(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    candidate_name = models.CharField(max_length=50)
    candidate_email = models.EmailField(max_length=30)
    candidate_phone = models.CharField(max_length=10)
    candidate_experience = models.CharField(max_length=20)
    candidate_interest = models.CharField(max_length=50)
    candidate_resume = models.FileField(upload_to="recruiter/pdfs")
    
    def __str__(self):
        return self.candidate_name