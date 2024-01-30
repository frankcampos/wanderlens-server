from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from wanderlensapi.models import Comment

class CommentView(ViewSet):
  def retrieve(self, request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    except comment.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
  
  def create(self, request):

      comment = Comment.objects.create(
          content=request.data["content"],
      )

      serializer = CommentSerializer(comment)
      return Response(serializer.data)
  
  def update(self, request, pk):
      comment = Comment.objects.get(pk=pk)
      comment.content = request.data["content"]
      comment.save()

      return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
      comment = Comment.objects.get(pk=pk)
      comment.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
  """JSON serializer for comments"""
  class Meta:
    model = Comment
    fields = ('id', 'user', 'post', 'content')
    depth = 1
