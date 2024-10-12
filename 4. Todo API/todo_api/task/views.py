from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema

# View to list and create tasks
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    filterset_fields = ['completed']

    @extend_schema(
        operation_id='List or Create Tasks',
        description='Lists tasks for the authenticated user or creates a new task.',
        request=TaskSerializer,
        responses={
            200: TaskSerializer(many=True),
            201: TaskSerializer,
        },
    )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

# View to retrieve, update, or delete a task
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  
