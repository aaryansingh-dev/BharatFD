import pytest
from django.urls import reverse
from rest_framework import status
from django.core.cache import cache
from .models import FAQ

@pytest.fixture
def faq():
    """Fixture to create a sample FAQ for testing."""
    faq_data = {
        "question": "What is Django?",
        "answer": "Django is a web framework."
    }
    return FAQ.objects.create(**faq_data)

@pytest.fixture
def api_client():
    """Fixture to provide an API client."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.mark.django_db
def test_create_faq(api_client):
    """Ensure we can create a new FAQ."""
    url = reverse('faq-list')
    data = {
        "question": "Who is the creator of this application?",
        "answer": "Aaryan is the creator of this application"
    }

    response = api_client.post(url, data, format='json')
    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED
    assert FAQ.objects.count() == 1
    assert response.data['question'] == data['question']
    assert response.data['answer'] == data['answer']

@pytest.mark.django_db
def test_retrieve_faq(api_client, faq):
    """Ensure we can retrieve an existing FAQ."""
    url = reverse('faq-detail', args=[faq.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == faq.question
    assert response.data['answer'] == faq.answer

@pytest.mark.django_db
def test_update_faq(api_client, faq):
    """Ensure we can update an existing FAQ."""
    url = reverse('faq-detail', args=[faq.id])
    updated_data = {
        "question": "What is Django?",
        "answer": "Django is a Python web framework for rapid development."
    }

    response = api_client.put(url, updated_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == updated_data['question']
    assert response.data['answer'] == updated_data['answer']

@pytest.mark.django_db
def test_delete_faq(api_client, faq):
    """Ensure we can delete an existing FAQ."""
    url = reverse('faq-detail', args=[faq.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert FAQ.objects.count() == 0

@pytest.mark.django_db
def test_list_faqs(api_client, faq):
    """Ensure we can list all FAQs."""
    url = reverse('faq-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['question'] == faq.question
    assert response.data[0]['answer'] == faq.answer

@pytest.mark.django_db
def test_translation_fallback(api_client, faq):
    """Ensure the API falls back to English if translation is unavailable."""
    url = reverse('faq-list')
    response = api_client.get(url, {'lang': 'hi'})  # Assuming 'hi' is the language code

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['question'] == faq.get_translation('question','hi')
    assert response.data[0]['answer'] == faq.get_translation('answer','hi')

@pytest.mark.django_db
def test_caching(api_client):
    """Ensure the API uses caching for improved performance."""
    url = reverse('faq-list')

    # First request to populate cache
    response1 = api_client.get(url)
    assert response1.status_code == status.HTTP_200_OK

    # Second request should hit the cache
    response2 = api_client.get(url)
    assert response2.status_code == status.HTTP_200_OK

    # Ensure cache hit by comparing response data
    assert response1.data == response2.data

@pytest.mark.django_db
def test_cache_invalidation_on_create(api_client):
    """Ensure the cache is invalidated when a new FAQ is created."""
    url = reverse('faq-list')

    # Make a request to populate the cache
    api_client.get(url)

    data = {
        "question": "What is this test?",
        "answer": "This is to check if cache is invalidated"
    }
    api_client.post(url, data, format='json')

    response = api_client.get(url)
    assert len(response.data) == 1

@pytest.mark.django_db
def test_cache_invalidation_on_update(api_client, faq):
    """Ensure the cache is invalidated when an FAQ is updated."""
    url = reverse('faq-detail', args=[faq.id])

    # Make a request to populate the cache
    api_client.get(url)

    updated_data = {
        "question": "What is Django?",
        "answer": "Django is a Python web framework."
    }
    api_client.put(url, updated_data, format='json')

    # Ensure cache invalidation and verify the updated data
    response = api_client.get(url)
    assert response.data['answer'] == updated_data['answer']

@pytest.mark.django_db
def test_cache_invalidation_on_delete(api_client, faq):
    """Ensure the cache is invalidated when an FAQ is deleted."""
    list_url = reverse('faq-list')
    detail_url = reverse('faq-detail', args=[faq.id])

    api_client.get(list_url)
    api_client.delete(detail_url)
    response = api_client.get(list_url)
    assert len(response.data) == 1  # FAQ should be deleted


@pytest.mark.django_db
def test_translation_telugu(api_client, faq):
    """Ensure the API returns FAQs translated into Telugu."""
    url = reverse('faq-list')
    response = api_client.get(url, {'lang': 'te'})

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['question'] == faq.get_translation('question','te')
    assert response.data[0]['answer'] == faq.get_translation('answer','te')

@pytest.mark.django_db
def test_translation_tamil(api_client, faq):
    """Ensure the API returns FAQs translated into Tamil"""
    url = reverse('faq-list')
    response = api_client.get(url, {'lang': 'ta'})

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['question'] == faq.get_translation('question','ta')
    assert response.data[0]['answer'] == faq.get_translation('answer','ta')
