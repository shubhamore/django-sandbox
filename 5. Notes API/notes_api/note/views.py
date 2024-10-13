from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsOwner
from .serializers import NoteSerializer
from .models import Note
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
import csv
from django.http import HttpResponse

# Create your views here.

class NoteListCreateView(ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class =  NoteSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','description']

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class NoteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
    
class NoteExportNotesCSV(APIView):
    permission_classes=[IsOwner]
    def get(self,request):
        notes = Note.objects.filter(owner=request.user)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="notes.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Created At', 'Last Modified'])  

        for note in notes:
            writer.writerow([note.title, note.description, note.created_at, note.last_modified])

        return response
    
class NoteExportNotesJSON(APIView):
    permission_classes=[IsOwner]
    def get(self,request):
        notes = Note.objects.filter(owner=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, content_type='application/json')
