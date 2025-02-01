from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

    def to_representation(self, object):
        # Get the language from the request
        lang = self.context['req'].query_params.get('lang', 'en')

        # Override the question and answer fields with the translated values
        finalObject= super().to_representation(object)
        finalObject['question'] = object.get_translation('question', lang)
        finalObject['answer'] = object.get_translation('answer', lang)

        return finalObject