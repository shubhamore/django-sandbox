from django.urls import path
from .views import NoteListCreateView, NoteRetrieveUpdateDestroyView, NoteExportNotesCSV, NoteExportNotesJSON

urlpatterns = [
    path('', NoteListCreateView.as_view(), name="note-list-create"),
    path('<int:pk>/', NoteRetrieveUpdateDestroyView.as_view(), name="note-detail"),
    path('export/csv/',NoteExportNotesCSV.as_view(),name='export-csv'),
    path('export/json/',NoteExportNotesJSON.as_view(),name='export-json'),
]
