from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage # Only needed for type hinting/default


# --- NEW HELPER FUNCTION ---
# This function is defined in settings.py and imported here via settings
def get_file_storage():
    """
    Returns the appropriate storage class instance based on settings.
    """
    return settings.FILE_STORAGE_FUNCTION() 
# ----------------------------


class DownloadEmail(models.Model):
    email = models.EmailField(max_length=254)
    document_name = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'download_emails'
        ordering = ['-downloaded_at']
        
    def __str__(self):
        return f"{self.email} - {self.document_name} - {self.downloaded_at}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Contact(models.Model):
    PRODUCT_CHOICES = [
        ('', 'Select a product'),
        ('MEA TRIAZINE 78%', 'MEA TRIAZINE 78%'),
        ('P-TOLUENE SULPHONIC ACID', 'P-TOLUENE SULPHONIC ACID'),
        ('DIISOPROPYLAMINO ETHYLYNE DIAMINE', 'DIISOPROPYLAMINO ETHYLYNE DIAMINE'),
        ('SODIUM CUMENE SULPHONATE', 'SODIUM CUMENE SULPHONATE'),
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


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name")

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


class Product(models.Model):

    
    priority = models.IntegerField(default=0, help_text="Higher number = higher priority")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    short_description = models.TextField()
    
    # Specifications
    purity = models.CharField(max_length=150, blank=True, null=True)
    packaging = models.CharField(max_length=150, blank=True, null=True)
    application = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    form = models.CharField(max_length=100, blank=True, null=True)
    cas_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="CAS Number")

    # Image URL (Google Drive direct link)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Google Drive direct image URL (use format: https://drive.google.com/uc?export=view&id=FILE_ID)"
    )
    
    # Files stored on Google Drive (if using gdstorage)
    video = models.FileField(
        upload_to='product_videos/',
        storage=settings.FILE_STORAGE_FUNCTION,  # ✅ Use callable from settings
        null=True,
        blank=True,
        help_text="Product demonstration video"
    )
    coa_pdf = models.FileField(
        upload_to='product_coa/',
        storage=settings.FILE_STORAGE_FUNCTION,  # ✅ Use callable from settings
        null=True,
        blank=True,
        help_text="Certificate of Analysis (PDF)"
    )
    tds_pdf = models.FileField(
        upload_to='product_tds/',
        storage=settings.FILE_STORAGE_FUNCTION,  # ✅ Use callable from settings
        null=True,
        blank=True,
        help_text="Technical Data Sheet (PDF)"
    )
    

    class Meta:
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name

    def has_downloads(self):
        """Check if product has downloadable files"""
        return bool(self.coa_pdf or self.tds_pdf)

    @property
    def specs(self):
        """Return product specifications as a dictionary"""
        specs = {}
        if self.purity:
            specs['Purity'] = self.purity
        if self.packaging:
            specs['Packaging'] = self.packaging
        if self.application:
            specs['Application'] = self.application
        if self.grade:
            specs['Grade'] = self.grade
        if self.form:
            specs['Form'] = self.form
        if self.cas_number:
            specs['CAS Number'] = self.cas_number
        return specs
    def get_direct_image_url(self):
        """Convert Google Drive URL to embeddable format"""
        if not self.image_url:
            return None
        
        import re
        
        file_id = None
        
        # Format 1: /file/d/FILE_ID/view
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', self.image_url)
        if match:
            file_id = match.group(1)
        return self.image_url