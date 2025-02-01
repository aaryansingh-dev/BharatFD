from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache

from .models import FAQ
from .serializers import FAQSerializer
from .utils.cache_setting import CACHE_TIMEOUT, CACHE_KEY_PREFIX
from .utils.language import LANGUAGES


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        cache_key = CACHE_KEY_PREFIX + lang
        data = cache.get(cache_key)

        if not data:
            data = FAQ.objects.all()
            cache.set(cache_key, data, timeout=CACHE_TIMEOUT * 60)

        return data

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['req'] = self.request
        return context

    def perform_create(self, serializer):
        instance = serializer.save()
        self.clear_cache()


    def perform_update(self, serializer):
        instance = serializer.save()
        self.clear_cache()


    def destroy(self, request, *args, **kwargs):
        if "all" in request.query_params:  # Check if the request asks to delete all
            FAQ.objects.all().delete()  # Delete all FAQs
            self.clear_cache()
            return Response({"message": "All FAQs deleted."}, 204)

        self.clear_cache()
        return super().destroy(request, *args, **kwargs)  # Delete single FAQ as usual

    def clear_cache(self):
        for lang in LANGUAGES:
            cache_key = CACHE_KEY_PREFIX + lang
            cache.delete(cache_key)
