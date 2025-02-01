from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

# Create your models here.
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

