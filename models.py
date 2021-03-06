from django.db import models
from django.db.models import Sum
from ckeditor.fields import RichTextField
from video_page.models import Video
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse

class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    

    def __str__(self):
        return self.name


class ProductCategory(MPTTModel):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    is_active_buy = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        try:
            if self.parent.parent:
                return reverse("products_parent2", kwargs={"category": self.slug, "parent":self.parent.slug, "parent2":self.parent.parent.slug})

            if self.parent:
                return reverse("products_parent", kwargs={"category": self.slug, "parent":self.parent.slug})
        except AttributeError:
            pass
        return reverse("products", kwargs={"category": self.slug, })
    


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = RichTextField()
    inner_number = models.CharField(max_length=50)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    old_price = models.IntegerField()
    promo_price = models.IntegerField(blank=True, null=True)
    in_stock = models.IntegerField()
    uploads = models.FileField(upload_to='uploads', blank=True)
    is_new_product = models.BooleanField()
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    weight = models.IntegerField()
    related_products = models.ManyToManyField("self", blank=True)
    bought_together = models.ManyToManyField("self", blank=True)
    slug = models.SlugField()
    meta_description = models.CharField(max_length=256)
    meta_keyword = models.CharField(max_length=50)
    meta_title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("products-detail", kwargs={
            "slug": self.slug,
            "category": self.category.slug,
            "parent": self.category.parent.slug,
            "parent2": self.category.parent.parent.slug
            }
        )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    age = models.IntegerField()

    class Meta:
        verbose_name = "ProductCharacteristic"
        verbose_name_plural = "ProductCharacteristics"



class PromotionPacket(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product)
    unit = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    you_save = models.CharField(max_length=50)
    upload = models.FileField(upload_to='uploads', blank=True)
    is_new = models.BooleanField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    weight = models.IntegerField()
    related_products = models.ManyToManyField('self', blank=True)
    compare = models.BooleanField()
    slug = models.SlugField()
    meta_description = models.CharField(max_length=256)
    meta_keyword = models.CharField(max_length=50)
    meta_title = models.CharField(max_length=50)
    is_acitve = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    class Meta:
        verbose_name = "Promotion Packet"
        verbose_name_plural = "Promotion Packets"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PromotionPacket_detail", kwargs={"slug": self.slug})

    @property
    def total_price(self):
        return sum(product.old_price for product in self.products.all())