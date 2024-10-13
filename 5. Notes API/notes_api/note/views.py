from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsOwner
from .serializers import NoteSerializer
from .models import Note
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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
    