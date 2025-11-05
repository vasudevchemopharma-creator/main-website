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
    priority = models.IntegerField(default=0, help_text="Higher number = higher priority (will appear first)")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    short_description = models.TextField()
    image = models.ImageField(
        upload_to='product_images/',
        null=True,
        blank=True,
        help_text="Recommended size: 354x200 pixels"
    )
    icon_text = models.CharField(
        max_length=10, 
        help_text="Short text shown if no image is uploaded",
        blank=True
    )
    purity = models.CharField(max_length=50, blank=True)
    packaging = models.CharField(max_length=100, blank=True)
    Product_Category = models.CharField(max_length=100, blank=True)
    application = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=100, blank=True)
    form = models.CharField(max_length=100, blank=True)
    cas_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name

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