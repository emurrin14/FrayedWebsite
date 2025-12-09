from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, ProductImage, Size, Color, Product_Variant, CustomUser, EmailVerificationToken, Cart

# Inline for Product Images so you can add/edit images directly in Product admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # number of extra blank forms
    fields = ('image', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return ""
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"

# Inline for Product Variants
class ProductVariantInline(admin.TabularInline):
    model = Product_Variant
    extra = 1
    autocomplete_fields = ['size', 'color']

# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock', 'isinstock', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'sku', 'description')
    list_filter = ('isinstock', 'tags')
    inlines = [ProductImageInline, ProductVariantInline]

# Register other models
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product_Variant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock')
    list_filter = ('size', 'color', 'product')
    search_fields = ('product__name',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'image')
    list_filter = ('product',)


class EmailVerificationTokenInline(admin.TabularInline):
    model = EmailVerificationToken
    extra = 0
    readonly_fields = ('token', 'created_at', 'expires_at', 'is_used', 'is_valid_display')
    fields = ('token', 'created_at', 'expires_at', 'is_used', 'is_valid_display')
    can_delete = False
    
    def is_valid_display(self, obj):
        if obj and obj.pk:
            is_valid = obj.is_valid()
            color = 'green' if is_valid else 'red'
            text = 'Valid' if is_valid else 'Expired/Used'
            return format_html('<span style="color: {};">{}</span>', color, text)
        return '-'
    is_valid_display.short_description = 'Status'

class CartInline(admin.TabularInline):
    model = Cart
    extra = 0
    readonly_fields = ('created_at', 'updated_at', 'total_items_display', 'total_price_display')
    fields = ('created_at', 'updated_at', 'total_items_display', 'total_price_display')
    can_delete = True
    
    def total_items_display(self, obj):
        if obj and obj.pk:
            return obj.total_items()
        return 0
    total_items_display.short_description = 'Items'
    
    def total_price_display(self, obj):
        if obj and obj.pk:
            return f"${obj.total_price():.2f}"
        return "$0.00"
    total_price_display.short_description = 'Total'



@admin.action(description='Mark selected users as email verified')
def verify_emails(modeladmin, request, queryset):
    queryset.update(email_verified=True)
    modeladmin.message_user(request, f'{queryset.count()} user(s) marked as email verified.')


@admin.action(description='Mark selected users as email unverified')
def unverify_emails(modeladmin, request, queryset):
    queryset.update(email_verified=False)
    modeladmin.message_user(request, f'{queryset.count()} user(s) marked as email unverified.')


@admin.action(description='Activate selected users')
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, f'{queryset.count()} user(s) activated.')


@admin.action(description='Deactivate selected users')
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, f'{queryset.count()} user(s) deactivated.')


@admin.action(description='Resend verification email to selected users')
def resend_verification_emails(modeladmin, request, queryset):
    count = 0
    for user in queryset.filter(email_verified=False):
        # Create new verification token
        token = EmailVerificationToken.objects.create(user=user)
        # Build verification URL
        verification_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': token.token})
        )
        # Send email
        try:
            send_mail(
                'Verify your email address',
                f'Please click the following link to verify your email address:\n\n{verification_url}\n\nThis link will expire in 24 hours.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            count += 1
        except Exception as e:
            modeladmin.message_user(request, f'Error sending email to {user.email}: {str(e)}', level='ERROR')
    modeladmin.message_user(request, f'Verification email sent to {count} user(s).')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'email_verified_badge', 'is_staff', 'is_active', 'date_joined', 'last_login', 'verification_tokens_count')
    list_filter = ('email_verified', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'password_display')
    actions = [verify_emails, unverify_emails, activate_users, deactivate_users, resend_verification_emails]
    inlines = [EmailVerificationTokenInline, CartInline]
    
    fieldsets = (
        (None, {'fields': ('email', 'password_display', 'password')}),
        ('Status', {'fields': ('email_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'email_verified', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    
    def email_verified_badge(self, obj):
        if obj.email_verified:
            return format_html('<span style="color: green; font-weight: bold;">✓ Verified</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Unverified</span>')
    email_verified_badge.short_description = 'Email Status'
    
    def verification_tokens_count(self, obj):
        count = obj.verification_tokens.count()
        if count > 0:
            active_count = sum(1 for token in obj.verification_tokens.all() if token.is_valid())
            return format_html('{} ({} active)', count, active_count)
        return '0'
    verification_tokens_count.short_description = 'Verification Tokens'
    
    def password_display(self, obj):
        if obj.pk:
            return format_html('<a href="../password/">Change password</a>')
        return 'Password will be set after saving'
    password_display.short_description = 'Password'


@admin.action(description='Mark selected tokens as used')
def mark_tokens_used(modeladmin, request, queryset):
    queryset.update(is_used=True)
    modeladmin.message_user(request, f'{queryset.count()} token(s) marked as used.')


@admin.action(description='Delete expired tokens')
def delete_expired_tokens(modeladmin, request, queryset):
    now = timezone.now()
    expired = queryset.filter(expires_at__lt=now)
    count = expired.count()
    expired.delete()
    modeladmin.message_user(request, f'{count} expired token(s) deleted.')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_short', 'status_badge', 'created_at', 'expires_at', 'is_used', 'is_expired')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at', 'is_valid_display', 'time_remaining')
    actions = [mark_tokens_used, delete_expired_tokens]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Token Information', {
            'fields': ('user', 'token', 'is_valid_display', 'time_remaining')
        }),
        ('Status', {
            'fields': ('is_used', 'created_at', 'expires_at')
        }),
    )
    
    def token_short(self, obj):
        if obj.token:
            return f"{obj.token[:20]}..."
        return '-'
    token_short.short_description = 'Token'
    
    def status_badge(self, obj):
        if obj.is_used:
            return format_html('<span style="color: gray;">Used</span>')
        elif obj.expires_at < timezone.now():
            return format_html('<span style="color: red;">Expired</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status_badge.short_description = 'Status'
    
    def is_expired(self, obj):
        return obj.expires_at < timezone.now()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
    
    def is_valid_display(self, obj):
        if obj and obj.pk:
            is_valid = obj.is_valid()
            color = 'green' if is_valid else 'red'
            text = 'Valid' if is_valid else 'Invalid (Expired or Used)'
            return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, text)
        return '-'
    is_valid_display.short_description = 'Validity'
    
    def time_remaining(self, obj):
        if obj and obj.pk and not obj.is_used:
            now = timezone.now()
            if obj.expires_at > now:
                delta = obj.expires_at - now
                hours = delta.total_seconds() / 3600
                if hours > 24:
                    return f"{int(hours / 24)} days"
                elif hours > 1:
                    return f"{int(hours)} hours"
                else:
                    minutes = int(delta.total_seconds() / 60)
                    return f"{minutes} minutes"
            else:
                return format_html('<span style="color: red;">Expired</span>')
        return '-'
    time_remaining.short_description = 'Time Remaining'
