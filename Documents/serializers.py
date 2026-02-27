from rest_framework import serializers
from .models import Document

class Document_Serializer(serializers.ModelSerializer):
    class Meta :
        model = Document
        fields = ["id","title","pdf","uploaded_at"]
    
    def validate_pdf(self, value):
        if value.content_type != "application/pdf":
            raise serializers.ValidationError("Only PDF files are allowed.")

        if value.size > 5 * 1024 * 1024:  
            raise serializers.ValidationError("File size must be under 5MB.")

        return value