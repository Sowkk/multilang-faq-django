from rest_framework import serializers
from .models import FAQ, FAQTranslation

#serializers - Convert Python objects to JSON (for sending responses) and vice versa (for receiving requests)
#used in view to return FAQs in JSON format  
class FAQTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQTranslation
        fields = ['language', 'question', 'answer']

class FAQSerializer(serializers.ModelSerializer):
    translations = FAQTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'translations']