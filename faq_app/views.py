from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache

from .models import FAQ
from .serializers import FAQSerializer
from .utils.cache_setting import CACHE_TIMEOUT, CACHE_KEY_PREFIX
from .utils.language import LANGUAGES


class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for FAQs, with caching support.

    Provides endpoints for creating, retrieving, updating, and deleting FAQs.
    """

    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        """
        Retrieve FAQs based on language query parameter and cache the result.

        Returns:
            queryset: List of FAQ objects filtered by language.
        """
        lang = self.request.query_params.get('lang', 'en')
        cache_key = CACHE_KEY_PREFIX + lang
        data = cache.get(cache_key)

        if not data:
            data = FAQ.objects.all()
            cache.set(cache_key, data, timeout=CACHE_TIMEOUT * 60)

        return data

    def get_serializer_context(self):
        """
        Add request object to serializer context.

        Returns:
            dict: Serializer context containing request object.
        """
        context = super().get_serializer_context()
        context['req'] = self.request
        return context

    def perform_create(self, serializer):
        """
        Perform additional actions after creating a new FAQ instance.

        Args:
            serializer: Serializer instance used to create FAQ.

        Returns:
            None
        """
        instance = serializer.save()
        self.clear_cache()

    def perform_update(self, serializer):
        """
        Perform additional actions after updating an existing FAQ instance.

        Args:
            serializer: Serializer instance used to update FAQ.

        Returns:
            None
        """
        instance = serializer.save()
        self.clear_cache()

    def destroy(self, request, *args, **kwargs):
        """
        Delete a single FAQ instance or all FAQs based on query parameters.

        Args:
            request: HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response object indicating success or failure.
        """
        if "all" in request.query_params:
            FAQ.objects.all().delete()
            self.clear_cache()
            return Response({"message": "All FAQs deleted."}, 204)

        self.clear_cache()
        return super().destroy(request, *args, **kwargs)

    def clear_cache(self):
        """
        Clear cache for all supported languages.

        Returns:
            None
        """
        for lang in LANGUAGES:
            cache_key = CACHE_KEY_PREFIX + lang
            cache.delete(cache_key)
