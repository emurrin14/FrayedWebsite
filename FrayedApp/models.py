from django.db import models
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(unique=True, blank=True)
  description = models.TextField()
  sku = models.CharField(max_length=50, unique=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField(default=0)
  isinstock = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  tags = TaggableManager()

  @property
  def image0(self):
    """ returns first image associated w product, if not image, none """
    first_image = self.images.first()
    return first_image.image if first_image else None
  
  def save(self, *args, **kwargs):
      if not self.slug:
          self.slug = slugify(self.title)
      
      self.IsInStock = self.stock > 0
      super().save(*args, **kwargs)
  
  def __str__(self):
      return self.title
  
class ProductImage(models.Model):
  product = models.ForeignKey(
     Product,
     on_delete=models.CASCADE,
     related_name="images"
  )
  image = models.ImageField (upload_to="products/")
  order = models.PositiveIntegerField(default=0, help_text="Set display order, 0 is primary image")

  def __str__(self):
    return f"Image For {self.product.name}"
  
  class Meta:
     """ Defines default ordering for image queries. """
     ordering = ['order']

class Size(models.Model):
  name = models.CharField(max_length=10)
  def __str__(self):
    return self.name
  
class Color(models.Model):
  name = models.CharField(max_length=10)
  def __str__(self):
    return self.name
  

class Product_Variant(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
  size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
  color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
  stock = models.PositiveIntegerField(default=0)