from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.html import strip_tags


# -------------------------------------------------------------------
# Helper: Dynamic storage (optional if using Google Drive or custom storage)
# -------------------------------------------------------------------
def get_file_storage():
    """Return storage callable from settings."""
    return settings.FILE_STORAGE_FUNCTION()


# -------------------------------------------------------------------
# Download Email Tracking
# -------------------------------------------------------------------
class DownloadEmail(models.Model):
    email = models.EmailField(max_length=254)
    document_name = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'download_emails'
        ordering = ['-downloaded_at']

    def __str__(self):
        return f"{self.email} - {self.document_name} - {self.downloaded_at:%Y-%m-%d %H:%M}"


# -------------------------------------------------------------------
# Contact Form Messages
# -------------------------------------------------------------------
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
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"

    @property
    def get_product_display_name(self):
        for choice in self.PRODUCT_CHOICES:
            if choice[0] == self.product:
                return choice[1]
        return self.product


# -------------------------------------------------------------------
# Product Category
# -------------------------------------------------------------------
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name")

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


# -------------------------------------------------------------------
# Product Master Model
# -------------------------------------------------------------------
class Product(models.Model):
    priority = models.IntegerField(default=0, help_text="Higher number = higher priority")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    short_description = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)

    purity = models.CharField(max_length=150, blank=True, null=True)
    packaging = models.CharField(max_length=150, blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    form = models.CharField(max_length=100, blank=True, null=True)

    cas_number = models.CharField(max_length=100, blank=True)
    formula = models.CharField(max_length=100, blank=True)
    appearance = models.CharField(max_length=200, blank=True)
    assay = models.CharField(max_length=100, blank=True)
    application = models.TextField(blank=True)
    molecular_weight = models.CharField(max_length=100, blank=True)
    density = models.CharField(max_length=100, blank=True)
    boiling_point = models.CharField(max_length=100, blank=True)
    melting_point = models.CharField(max_length=100, blank=True)

    # Image (with optional Google Drive URL)
    image_url = models.URLField(
        max_length=500, blank=True, null=True,
        help_text="https://lh3.googleusercontent.com/d/ID)"
    )
    main_image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    gallery_image_1 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    gallery_image_2 = models.ImageField(upload_to='products/images/', blank=True, null=True)

    # Files and media
    video = models.FileField(
        upload_to='product_videos/',
        storage=get_file_storage,
        null=True, blank=True,
        help_text="Product demonstration video"
    )
    coa_pdf = models.FileField(
        upload_to='product_coa/',
        storage=get_file_storage,
        null=True, blank=True,
        help_text="Certificate of Analysis (PDF)"
    )
    tds_pdf = models.FileField(
        upload_to='product_tds/',
        storage=get_file_storage,
        null=True, blank=True,
        help_text="Technical Data Sheet (PDF)"
    )

    # Certifications & SEO
    iso_certifications = models.CharField(max_length=255, blank=True)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    # Schema / reviews
    schema_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0,
                                        help_text='Average rating for schema.org (0.00 - 5.00)')
    schema_review_count = models.IntegerField(default=0, help_text='Number of reviews for schema.org')

    # Control fields
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name

    # --- Utility methods ---
    def has_downloads(self):
        """Check if product has downloadable files."""
        return bool(self.coa_pdf or self.tds_pdf)

    @property
    def specs(self):
        """Return product specifications as a dictionary."""
        specs = {}
        if self.purity:
            specs['Purity'] = self.purity
        if self.packaging:
            specs['Packaging'] = self.packaging
        if self.grade:
            specs['Grade'] = self.grade
        if self.form:
            specs['Form'] = self.form
        if self.cas_number:
            specs['CAS Number'] = self.cas_number
        if self.application:
            specs['Application'] = self.application
        return specs

    def get_direct_image_url(self):
        """Convert Google Drive URL to embeddable format if applicable."""
        if not self.image_url:
            return None
        import re
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', self.image_url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        return self.image_url

    def save(self, *args, **kwargs):
        """Auto-generate meta_description when empty using short/detailed description."""
        # Prefer existing value
        if not self.meta_description:
            # pick the most descriptive field available
            source = self.short_description or self.detailed_description or ''
            # strip any HTML and truncate to ~150 chars for SERP
            clean = strip_tags(source)[:160].strip()
            # ensure we don't cut in the middle of a word if possible
            if len(clean) > 150:
                # cut at last space before 150
                idx = clean.rfind(' ', 0, 150)
                if idx > 50:
                    clean = clean[:idx]
            self.meta_description = clean
        super().save(*args, **kwargs)


# -------------------------------------------------------------------
# Product FAQs
# -------------------------------------------------------------------
class ProductFAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.question[:40]}"


# -------------------------------------------------------------------
# Product Applications
# -------------------------------------------------------------------
class ProductApplication(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='applications')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.title}"


# -------------------------------------------------------------------
# Company Informations , FAQs, Blogs Etc.
# -------------------------------------------------------------------

class CompanyInformation(models.Model):
    company_name = models.CharField(max_length=200)
    address = models.TextField()
    sales_phone = models.CharField(max_length=50)
    sales_email = models.EmailField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    whatsapp_number = models.URLField(max_length=50, blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    base_url = models.URLField(blank=True, null=True)
    # Site-wide SEO fields
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.company_name
    
class CompanyFAQ(models.Model):
    CompanyInformation = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.CompanyInformation.company_name} - {self.question[:40]}"
    
class CompanyBlog(models.Model):
    CompanyBlog = models.ForeignKey(CompanyInformation, on_delete=models.CASCADE, related_name='Blogs')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    # SEO fields
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.meta_description:
            clean = strip_tags(self.content)[:160].strip()
            if len(clean) > 150:
                idx = clean.rfind(' ', 0, 150)
                if idx > 50:
                    clean = clean[:idx]
            self.meta_description = clean
        super().save(*args, **kwargs)
    
class ProductBlog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Blogs')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    # SEO fields
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.meta_description:
            clean = strip_tags(self.content)[:160].strip()
            if len(clean) > 150:
                idx = clean.rfind(' ', 0, 150)
                if idx > 50:
                    clean = clean[:idx]
            self.meta_description = clean
        super().save(*args, **kwargs)