# models.py
from django.db import models
from django.utils import timezone


class DownloadEmail(models.Model):
    email = models.EmailField(max_length=254)
    document_name = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)  # This will use current timezone
    
    class Meta:
        db_table = 'download_emails'
        ordering = ['-downloaded_at']
        
    def __str__(self):
        return f"{self.email} - {self.document_name} - {self.downloaded_at}"
    
    def save(self, *args, **kwargs):
        # Ensure we're using the current local timezone
        if not self.downloaded_at:
            self.downloaded_at = timezone.now()
        super().save(*args, **kwargs)


class Contact(models.Model):
    PRODUCT_CHOICES = [
        ('', 'Select a product'),
        ('acetic-acid', 'Acetic Acid'),
        ('sodium-hydroxide', 'Sodium Hydroxide'),
        ('sulfuric-acid', 'Sulfuric Acid'),
        ('hydrochloric-acid', 'Hydrochloric Acid'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    company = models.CharField(max_length=150, blank=True, null=True, verbose_name="Company Name")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    product = models.CharField(max_length=50, choices=PRODUCT_CHOICES, blank=True, null=True, verbose_name="Product Interest")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def get_product_display_name(self):
        """Return the display name for the selected product"""
        for choice in self.PRODUCT_CHOICES:
            if choice[0] == self.product:
                return choice[1]
        return self.product