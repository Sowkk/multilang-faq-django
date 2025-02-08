from rest_framework import viewsets
from .models import FAQ, FAQTranslation
from .serializers import FAQSerializer
from rest_framework.decorators import action
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
  
# Create your views here.
class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request):
        try:
            language = request.query_params.get('lang', 'en')

            if language not in ['en', 'hi', 'bn', 'te', 'ta', 'ur', 'ml', 'ko', 'zh-TW']:
                return Response(
                    {'error': 'Unsupported language'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # check in cache
            cache_key = f'faqs_{language}'
            cached_data = cache.get(cache_key)
            
            if cached_data is not None:
                return Response(cached_data)
            
            # If not in cache, get from database
            data = []
            if language == 'en':
                faqs = FAQ.objects.all()
                for faq in faqs:
                    # Use base FAQ model for English
                    data.append({
                        'id': faq.id,
                        'question': faq.question,
                        'answer': faq.answer,
                        'language': 'en'
                    })
            else:
                # Use translations for other languages
                translations = FAQTranslation.objects.filter(language=language)
                for translation in translations:
                    data.append({
                        'id': translation.faq.id,
                        'question': translation.question,
                        'answer': translation.answer,
                        'language': translation.language
                    })
            # Store in cache
            cache.set(cache_key, data, timeout=settings.CACHE_TTL)
            return Response(data)
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        