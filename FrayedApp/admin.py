from django.contrib import admin
from .models import Product, ProductImage, Size, Color, Product_Variant

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
