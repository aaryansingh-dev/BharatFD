from django.db import models
from ckeditor.fields import RichTextField

from .utils.language import LANGUAGES, translate


# Create your models here.
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    def save(self, *args, **kwargs):
        for lang in LANGUAGES:
            attr_question= f'question_{lang}'
            attr_answer = f'answer_{lang}'

            if not getattr(self, attr_question):
                setattr(self, attr_question, translate(self.question, lang))
            if not getattr(self, attr_answer):
                setattr(self, attr_answer, translate(self.answer, lang))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


