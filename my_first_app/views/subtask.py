from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from my_first_app.models import SubTask
from my_first_app.serializers.subtask import SubTaskCreateSerializer, SubTaskSerializer
from my_first_app.permissions import IsOwnerOrAdminOrReadOnly


class SubTaskListCreateViewGeneric(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubTask.objects.all().order_by("created_at")
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']  # Поля для поиска
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        return SubTaskCreateSerializer if self.request.method == "POST" else SubTaskSerializer

class SubTaskDetailUpdateDeleteViewGeneric(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        return SubTaskCreateSerializer if self.request.method in {"PUT", "PATCH"} else SubTaskSerializer

