from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from wanderlensapi.models import Post, User

class PostView(ViewSet):
  def retrieve (self, request, pk):
    post = Post.objects.get(pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)

  def list(self, request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    user = User.objects.get(pk=request.data["userId"])
    
    post = Post.objects.create(
      user = user,
      title = request.data["title"],
      image_url=request.data["imageUrl"],
      content = request.data["content"]
    )
    
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data)
  
  def update(self, request, pk):
    post = Post.objects.get(pk=pk)
    post.title=request.data["title"]
    post.image_url=request.data["imageUrl"]
    post.content = request.data["content"]
  
    post.save()
    return Response(None, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ('id', 'user', 'title', 'image_url', 'content')
    depth = 1
