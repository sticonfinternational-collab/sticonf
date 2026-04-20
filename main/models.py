from django.db import models
from django.utils import timezone


class SponsorshipTier(models.Model):
    """Sponsorship tier options"""
    TIER_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    
    tier_name = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount in NGN")
    description = models.TextField()
    
    def __str__(self):
        return f"{self.get_tier_name_display()} (₦{self.amount:,.0f})"


class Sponsorship(models.Model):
    """Track sponsorship payments and details"""
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('failed', 'Payment Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Company/Organization Info
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Nigeria')
    
    # Sponsorship Info
    tier = models.ForeignKey(SponsorshipTier, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount in NGN")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment Info
    reference = models.CharField(max_length=100, unique=True, help_text="Flutterwave transaction reference")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.tier.get_tier_name_display()}"
    
    def mark_as_paid(self):
        """Mark sponsorship as paid"""
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()


class Registration(models.Model):
    """Track conference registration details"""
    CATEGORY_CHOICES = [
        ('student', 'Student'),
        ('academic', 'Academic/Researcher'),
        ('industry', 'Industry Professional'),
        ('government', 'Government'),
        ('investor', 'Investor'),
        ('startup', 'Startup Founder'),
        ('other', 'Other'),
    ]
    
    INTEREST_CHOICES = [
        ('ai_ml', 'AI & Machine Learning'),
        ('iot', 'IoT & Connected Devices'),
        ('blockchain', 'Blockchain & Web3'),
        ('biotech', 'Biotechnology'),
        ('cleantech', 'Clean Technology'),
        ('agritech', 'AgriTech'),
        ('fintech', 'FinTech'),
        ('other', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Professional Information
    organisation = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    country = models.CharField(max_length=100, blank=True, default='Nigeria')
    
    # Interests
    interest = models.CharField(max_length=200, choices=INTEREST_CHOICES, default='other')
    
    # Status
    brevo_synced = models.BooleanField(default=False, help_text="Whether synced to Brevo mailing list")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Contact(models.Model):
    """Track contact form submissions"""
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('sponsorship', 'Sponsorship'),
        ('speaking', 'Speaking Opportunity'),
        ('partnership', 'Partnership'),
        ('media', 'Media/Press'),
        ('other', 'Other'),
    ]
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Company Information
    organisation = models.CharField(max_length=200, blank=True)
    
    # Message
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    interest = models.TextField(help_text="Message/Inquiry details")
    
    # Status
    read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)
    response_notes = models.TextField(blank=True, help_text="Internal notes on response")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.category}"
