from pathlib import Path

from django.http import FileResponse, HttpResponseServerError
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from miqa.core.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'name', 'scan']


class ImageViewSet(ListModelMixin, GenericViewSet):
    queryset = Image.objects.all()

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['scan']

    permission_classes = [AllowAny]
    serializer_class = ImageSerializer

    @action(detail=True)
    def download(self, request, pk=None, **kwargs):
        image: Image = self.get_object()
        path: Path = image.path
        if not path.is_file():
            return HttpResponseServerError('File no longer exists.')

        fd = open(path, 'rb')
        resp = FileResponse(fd, filename=image.name)
        resp['Content-Length'] = image.size
        return resp
