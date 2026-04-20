from django.contrib import admin
from django.utils.html import format_html
from main.models import SponsorshipTier, Sponsorship, Registration, Contact


# ===== SPONSORSHIP ADMIN =====
@admin.register(SponsorshipTier)
class SponsorshipTierAdmin(admin.ModelAdmin):
    list_display = ('get_tier_display', 'amount', 'description')
    
    def get_tier_display(self, obj):
        return obj.get_tier_name_display()
    get_tier_display.short_description = 'Tier'


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'tier', 'amount', 'get_status_badge', 'email', 'created_at')
    list_filter = ('status', 'tier', 'created_at', 'country')
    search_fields = ('company_name', 'contact_name', 'email', 'reference')
    readonly_fields = ('reference', 'transaction_id', 'created_at', 'updated_at', 'paid_at')
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'contact_name', 'email', 'phone', 'country')
        }),
        ('Sponsorship Details', {
            'fields': ('tier', 'amount', 'status')
        }),
        ('Payment Information', {
            'fields': ('reference', 'transaction_id', 'paid_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'paid': '#00C851',
            'failed': '#FF4444',
            'cancelled': '#ff0000',
        }
        return format_html(
            '<span style="background-color:{}; color:white; padding:3px 10px; border-radius:3px; font-weight:bold;">{}</span>',
            colors.get(obj.status, "#999"),
            obj.get_status_display()
        )
    get_status_badge.short_description = 'Payment Status'


# ===== REGISTRATION ADMIN =====
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'category', 'country', 'get_brevo_status', 'created_at')
    list_filter = ('category', 'country', 'interest', 'brevo_synced', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'organisation')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('organisation', 'category', 'country')
        }),
        ('Interests', {
            'fields': ('interest',)
        }),
        ('Sync Status', {
            'fields': ('brevo_synced',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    get_full_name.short_description = 'Name'
    
    def get_brevo_status(self, obj):
        status = '✓ Synced' if obj.brevo_synced else '✗ Not Synced'
        color = '#00C851' if obj.brevo_synced else '#FF4444'
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            status
        )
    get_brevo_status.short_description = 'Brevo Status'
    
    actions = ['mark_brevo_synced']
    
    def mark_brevo_synced(self, request, queryset):
        updated = queryset.update(brevo_synced=True)
        self.message_user(request, f'{updated} registrations marked as synced to Brevo.')
    mark_brevo_synced.short_description = 'Mark selected as Brevo synced'


# ===== CONTACT ADMIN =====
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'category', 'get_read_status', 'get_responded_status', 'created_at')
    list_filter = ('category', 'read', 'responded', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'organisation', 'interest')
    readonly_fields = ('created_at', 'updated_at', 'interest')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Company Information', {
            'fields': ('organisation',)
        }),
        ('Inquiry Details', {
            'fields': ('category', 'interest')
        }),
        ('Response Status', {
            'fields': ('read', 'responded')
        }),
        ('Response Notes', {
            'fields': ('response_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    get_full_name.short_description = 'Name'
    
    def get_read_status(self, obj):
        status = '✓ Read' if obj.read else '○ Unread'
        color = '#666' if obj.read else '#FF9900'
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            status
        )
    get_read_status.short_description = 'Read Status'
    
    def get_responded_status(self, obj):
        status = '✓ Responded' if obj.responded else '✗ Pending'
        color = '#00C851' if obj.responded else '#FF4444'
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            status
        )
    get_responded_status.short_description = 'Response'
    
    actions = ['mark_as_read', 'mark_as_responded']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(read=True)
        self.message_user(request, f'{updated} inquiries marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_responded(self, request, queryset):
        updated = queryset.update(responded=True)
        self.message_user(request, f'{updated} inquiries marked as responded.')
    mark_as_responded.short_description = 'Mark selected as responded'


