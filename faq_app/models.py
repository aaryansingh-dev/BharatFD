from django.db import models
from ckeditor.fields import RichTextField

from .utils.language import LANGUAGES, translate


# Create your models here.
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()


