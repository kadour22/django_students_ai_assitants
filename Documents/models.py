# models.py
from django.db import models
from django.core.validators import FileExtensionValidator

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(
        upload_to="pdfs/",
        validators=[FileExtensionValidator(['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title