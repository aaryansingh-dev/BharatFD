from django.db import models
from ckeditor.fields import RichTextField

from .utils.language import LANGUAGES, translate


# Create your models here.
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    question_en = models.TextField(blank=True, null=True)
    answer_en = RichTextField(blank=True, null=True)

    question_hi = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)

    question_ta = models.TextField(blank=True, null=True)
    answer_ta = RichTextField(blank=True, null=True)

    question_bn = models.TextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)

    question_mr = models.TextField(blank=True, null=True)
    answer_mr = RichTextField(blank=True, null=True)

    question_te = models.TextField(blank=True, null=True)
    answer_te = RichTextField(blank=True, null=True)


    def save(self, *args, **kwargs):
            for lang in LANGUAGES:
                attr_question= f'question_{lang}'
                attr_answer = f'answer_{lang}'

                # sets the values to new text
                setattr(self, attr_question, translate(self.question, lang))  # Always update
                setattr(self, attr_answer, translate(self.answer, lang))
            super().save(*args, **kwargs)

    def get_translation(self, field, lang):
        field_name = f'{field}_{lang}'
        if getattr(self, field_name):
            return getattr(self, field_name)
        elif getattr(self,f'{field}_en' ):
            # fall back to english
            return getattr(self,f'{field}_en' )
        else:
            # if english not found, fallback to original answer
            return getattr(self,field)

    def __str__(self):
        return self.question


