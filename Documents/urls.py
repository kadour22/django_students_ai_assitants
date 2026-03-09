from django.urls import path
from .views import DocumentAPIView, DocumentGenerateAPIView
urlpatterns = [
    path('documents/', DocumentAPIView.as_view(), name='document-list-create'),
    path('documents/<int:document_id>/', DocumentAPIView.as_view(), name='document-detail-delete'),
    path('documents/<int:document_id>/generate/', DocumentGenerateAPIView.as_view(), name='document-generate'),
]