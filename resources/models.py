from django.db import models
from django.conf import settings


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('protocols', 'Protocols'),
        ('templates', 'Templates'),
        ('articles', 'Articles'),
        ('tools', 'Tools'),
        ('links', 'Links'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
