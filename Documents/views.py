import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Documents.Agent.AI import AI
from Documents.utils import extract_text_from_pdf
from .models import Document
from .serializers import Document_Serializer, DocumentList_Serializer
from Documents.services.document_service import DocumentService


class DocumentAPIView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_service = DocumentService()

    def get(self, request, document_id=None):
        if document_id:
            document = self.document_service.get_document_by_id(document_id)
            if document:
                serializer = Document_Serializer(document)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            documents = self.document_service.get_all_documents()
            serializer = DocumentList_Serializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Document_Serializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data["title"]
            pdf_file = serializer.validated_data["pdf"]
            document = self.document_service.create_document(title, pdf_file)
            response_serializer = Document_Serializer(document)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, document_id):
        success = self.document_service.delete_document(document_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)


class DocumentGenerateAPIView(APIView):
    """Generate a resume + quiz from an existing uploaded PDF document."""

    def post(self, request, document_id):
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)

        raw_text = extract_text_from_pdf(document.pdf.path)
        if not raw_text.strip():
            return Response(
                {"detail": "Unable to extract text from PDF."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate content using the AI helper
        ai = AI(api_key=os.getenv("OPENAI_API_KEY"))
        resume = ai.generate_resume(raw_text)
        quiz = ai.generate_quiz(raw_text)

        return Response(
            {
                "resume": resume,
                "quiz": quiz,
            },
            status=status.HTTP_200_OK,
        )

