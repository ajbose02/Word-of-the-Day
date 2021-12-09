from django.db import models
from datetime import date

# Create your models here.
class word_class(models.Model):
    word = models.CharField(max_length=200)
    definition = models.TextField(max_length=500)
    speech = models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=False)
