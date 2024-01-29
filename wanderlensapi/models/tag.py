from django.db import models

class Tag(models.Model):
    """Model for tag table"""

    label = models.CharField(max_length=50)
