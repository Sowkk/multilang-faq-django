from django.contrib import admin
from .models import FAQ, FAQTranslation
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

# Register your models here.

@admin.register(FAQTranslation)
class FAQTranslationAdmin(admin.ModelAdmin):
    list_display = ['faq', 'language', 'question_preview']
    list_filter = ['language']
    search_fields = ['faq__question', 'question', 'answer', 'language']
    readonly_fields = ['language']
    
    def question_preview(self, obj):
        return obj.question[:100] + '...' if len(obj.question) > 100 else obj.question
    question_preview.short_description = 'Translated'

    class Media:
        css = {
            'all': [
                'admin/css/custom_filters.css',
            ]
        }

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'created_at', 'view_translations']
    list_filter = ['created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at']
    
    def question_preview(self, obj):
        return obj.question[:100] + '...' if len(obj.question) > 100 else obj.question
    question_preview.short_description = 'Question'
    
    def view_translations(self, obj):
        url = (
            reverse("admin:faqs_faqtranslation_changelist")
            + "?"
            + urlencode({"faq__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">View Translations</a>', url)
    view_translations.short_description = 'Translations'

    class Media:
        css = {
            'all': [
                'admin/css/custom_filters.css',
            ]
        }