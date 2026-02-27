from rest_framework import serializers
from .models import Document

class Document_Serializer(serializers.ModelSerializer):
    class Meta :
        model = Document
        fields = ["id","title","pdf","uploaded_at"]