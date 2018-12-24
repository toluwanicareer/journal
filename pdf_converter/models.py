from django.db import models

# Create your models here.

class Token(models.Model):
    token=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

