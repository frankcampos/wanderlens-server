from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ..models import Tag

class TagView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for a single order type
          
        returns:
        Response -- JSON Serialzied order"""
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Order"""
    class Meta:
        model = Tag
        fields = ("id", "label")
