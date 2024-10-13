from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsOwner
from .serializers import NoteSerializer, TagSerializer
from .models import Note, Tag
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
import csv
from django.http import HttpResponse
from rest_framework.response import Response

# Create your views here.

class NoteListCreateView(ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class =  NoteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['tags']
    search_fields = ['title','description']

    def get_queryset(self):
        user = self.request.user
        queryset = Note.objects.filter(owner=user)
        tag_names = self.request.query_params.getlist('tags')
        if tag_names:
            tags = Tag.objects.filter(name__in=tag_names, owner=user)
            if tags.exists():
                queryset = queryset.filter(tags__in=tags)
        if not queryset.exists():
            return Note.objects.none()  # Or handle as you prefer
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        notes_data = serializer.data
        user_tags = Tag.objects.filter(owner=request.user)
        tags_names = [tag.name for tag in user_tags]
        response_data = self.get_paginated_response(notes_data)
        response_data.data['tags'] = tags_names
        return response_data
        
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
