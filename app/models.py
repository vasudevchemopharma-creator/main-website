# models.py
from django.db import models
from django.utils import timezone

class DownloadEmail(models.Model):
    email = models.EmailField(max_length=254)
    document_name = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    downloaded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'download_emails'
        ordering = ['-downloaded_at']
        
    def __str__(self):
        return f"{self.email} - {self.document_name} - {self.downloaded_at}"