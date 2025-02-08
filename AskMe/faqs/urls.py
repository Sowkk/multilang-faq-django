from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet

router = DefaultRouter()
router.register(r'faqs', FAQViewSet)
# The DefaultRouter creates these URL patterns:

# faqs/ → 'faq-list'
# faqs/<pk>/ → 'faq-detail'

urlpatterns = [
    path('', include(router.urls)), 
]