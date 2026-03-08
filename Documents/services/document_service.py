from typing import Optional, List, Dict, Any
from django.db.models import Count, Q
from django.core.cache import cache
from django.db import models

from Documents.base.base_service import BaseService
from Documents.models import Document

class DocumentService(BaseService) :

    def __init__(self):
        super().__init__()
        self.document_cache_timeout = self.cache_timeout.get('documents_lists',1800)
    
    def get_all_documents(self) -> List[Document]:
        cache_key = self.get_cache_key('all_documents')

        cached_document = self.get_from_cache(cache_key)
        if cached_document:
            return cached_document

        query = Document.objects.all().order_by('-uploaded_at')
        documents = list(query)

        self.set_cache(cache_key, documents, timeout=self.document_cache_timeout)
        return documents

    def create_document(self, title: str, pdf_file) -> Document:
        document = Document.objects.create(title=title, pdf=pdf_file)
        self.delete_cache_pattern('all_documents*')
        return document
    
    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        cache_key = self.get_cache_key('document', id=document_id)

        cached_document = self.get_from_cache(cache_key)
        if cached_document:
            return cached_document

        try:
            document = Document.objects.get(id=document_id)
            self.set_cache(cache_key, document, timeout=self.document_cache_timeout)
            return document
        except Document.DoesNotExist:
            return None
    
    def delete_document(self, document_id: int) -> bool:
        try:
            document = Document.objects.get(id=document_id)
            document.delete()
            self.delete_cache_pattern('all_documents*')
            self.delete_cache_pattern(f'document_id:{document_id}*')
            return True
        except Document.DoesNotExist:
            return False
