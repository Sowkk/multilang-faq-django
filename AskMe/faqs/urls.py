from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet

router = DefaultRouter()
router.register(r'faqs', FAQViewSet)
# faqs/ → 'faq-list'
# faqs/<pk>/ → 'faq-detail'
#register -> ViewSets
#automatically generates URLs for API views of CRUD operations

#maps URLs to views i.e only single http method
urlpatterns = [
    path('', include(router.urls)), 
]