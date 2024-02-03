from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from wanderlensapi.models import Post, User, PostTag, Tag, Comment

class PostView(ViewSet):
  
  
  @action(methods=['post'], detail=True)
  def add_tag_to_post(self, request, pk):
      post = Post.objects.get(pk=pk)
      tag = Tag.objects.get(id=request.data['tagId'])
      try:
        PostTag.objects.get(post=post, tag=tag)
        return Response({'message: This post already has this tag.'})
      except PostTag.DoesNotExist:
        PostTag.objects.create(
            post=post,
            tag=tag
        )
        return Response(None, status=status.HTTP_200_OK)

  @action(methods=['delete'], detail=True)
  def remove_tag_from_post(self, request, pk):
      post = Post.objects.get(pk=pk)
      post_tag = PostTag.objects.get(post=post, tag=request.data['tagId'])
      post_tag.delete()

      return Response(None, status=status.HTTP_200_OK)
  
  def retrieve (self, request, pk):
    post = Post.objects.get(pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)

  def list(self, request):
    posts = Post.objects.all()
    user = request.query_params.get('user', None)
    if user is not None:
      posts = posts.filter(user=user)
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

class PostTagSerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField(source='tag.id')
  label = serializers.ReadOnlyField(source='tag.label')
  class Meta:
    model = PostTag
    fields = ('id', 'label')
    
class PostCommentSerializer(serializers.ModelSerializer):
  class Meta:
    model= Comment
    fields=('id','user','content')
    depth = 1
class PostSerializer(serializers.ModelSerializer):
  tags = PostTagSerializer(many=True, read_only=True)
  comments = PostCommentSerializer(many=True, read_only=True)
  class Meta:
    model = Post
    fields = ('id', 'user', 'title', 'image_url', 'content', 'comments', 'tags')
    depth = 1
