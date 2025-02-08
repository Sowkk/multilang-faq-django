# Create your tests here.
from django.urls import reverse
from rest_framework import status
from .models import FAQ, FAQTranslation
from django.core.cache import cache
import pytest
import json

@pytest.mark.django_db
class TestFAQAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Create a test FAQ before each test
        self.faq = FAQ.objects.create(
            question="Test FAQ?",
            answer="Test Answer"
        )
        yield
        #Cleanup after each test
        FAQ.objects.all().delete()
        cache.clear()

    def test_caching(self, client):
        url = reverse('faq-list')

        # Clear any existing cache
        cache.delete('faqs_en')

        # First request - should hit database     
        response1 = client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        
        # Check cache
        cached_data = cache.get('faqs_en')
        assert cached_data is not None
        
         # Second request - should hit cache
        response2 = client.get(url)
        assert response2.data == response1.data
   

    def test_create_faq(self, client):
        url = reverse('faq-list')
        data = {
            "question": "New Test Question?",
            "answer": "New Test Answer"
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.count() == 2 #setup+new

    def test_update_faq(self, client):
        url = f'/api/faqs/{self.faq.id}/'
        data = {
            "question": "Updated Question",
            "answer": "Updated Answer"
        }
        response = client.put(url, json.dumps(data), content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        self.faq.refresh_from_db()
        assert self.faq.question == "Updated Question"

    def test_delete_faq(self, client):
        url = f'/api/faqs/{self.faq.id}/'
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert FAQ.objects.count() == 0

    def test_translation_creation(self):
        faq = FAQ.objects.create(
            question="Test Translns Creation Question?",
            answer="Test Translns Creation Answer"
        )
        translations = faq.translations.all()
        languages = ['hi', 'bn', 'te', 'ta', 'ur', 'ml', 'ko', 'zh-TW']
        assert translations.count() == len(languages)

    def test_invalid_language(self, client):
        response = client.get(f"{reverse('faq-list')}?lang=invalid")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_language_specific_responses(self, client):
        faq = FAQ.objects.create(
            question="Language Test?",
            answer="Language Answer"
        )
        
        # Test different languages
        languages = ['en', 'hi', 'bn']
        for lang in languages:
            response = client.get(f"{reverse('faq-list')}?lang={lang}")
            assert response.status_code == status.HTTP_200_OK
            if lang == 'en':
                assert response.data[0]['question'] == faq.question
            else:
                assert response.data[0]['language'] == lang
