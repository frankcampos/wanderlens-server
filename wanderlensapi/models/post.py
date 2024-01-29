from django.db import models
from .user import User

class Post(models.Model):
    """Model for Post table"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image_url = models.URLField()
    content = models.TextField()
