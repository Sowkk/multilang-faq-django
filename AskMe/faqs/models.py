from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django.utils import timezone
# Create your models here.

def translate_text(text, dest_lang):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=dest_lang)
        return translation.text
    except Exception as e:
        return text  # fallback to english if translation fails
    
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
                        
            # translate to other languages
            languages = ['hi', 'bn', 'te', 'ta', 'ur', 'ml', 'ko', 'zh-TW']
            for lang in languages:
                translated_question = translate_text(self.question, lang)
                translated_answer = translate_text(self.answer, lang)
                
                FAQTranslation.objects.create(
                    faq=self,
                    language=lang,
                    question=translated_question,
                    answer=translated_answer
                )
    def __str__(self):
        return self.question[:50]
    

class FAQTranslation(models.Model):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=10)
    question = models.TextField()
    answer = RichTextField() 

    class Meta:
        unique_together = ['faq', 'language']
        indexes = [
            models.Index(fields=['language']),
        ]
    def __str__(self):
        return f"{self.language} translation of FAQ {self.faq_id}"
    
