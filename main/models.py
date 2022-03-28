from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser

# Create your models here.



#Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))
    
    class Meta:
        verbose_name_plural = "1. Banners"

    def __str__(self):
        return self.alt_text

#Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    class Meta:
        verbose_name_plural = "2. Categories"

    def __str__(self):
        return self.title



#Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural = "3. Brands"

    def __str__(self):
        return self.title


#Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    def color_bg(self):
        return mark_safe('<div style="width:50px; height:30px; background:%s;"></div>' % (self.color_code))

    class Meta:
        verbose_name_plural = "4. Colors" 

    def __str__(self):
        return self.title

    
#Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "5. Sizes"
    def __str__(self):
        return self.title



#Product Model
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=400)
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "6. Products"

    def __str__(self):
        return self.title


#Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="product_imgs/",null=True)
    price=models.DecimalField(decimal_places=2,max_digits=8)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name_plural = "7. Product Attributes"

    def __str__(self):
        return self.product.title

    

#Custom User Model
class CustomUser(AbstractUser):
    phone_no = models.CharField(max_length=10,null=True)
    is_delboy = models.BooleanField('is_deliveryBoy',default=False)



