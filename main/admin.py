from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category,Brand,Color, ProductAttribute,Size,Product,Banner,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
from .models import CustomUser
from .forms import SignupForm
# Register your models here.

admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Wishlist)


class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','brand','status','is_featured')
    list_editable=('status','is_featured',)
admin.site.register(Product,ProductAdmin)

#Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','product','price','color','size','image_tag')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

#admin is tightly coupled to the default user model. so extending UserAdmin class to use the new customuser model
class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    model = CustomUser
    list_display = ['username', 'phone_no', 'is_delboy', ]

admin.site.register(CustomUser,CustomUserAdmin)


#order
class CartOrderAdmin(admin.ModelAdmin):
    list_editable=('paid_status','order_status','order_status')
    list_display=('id','user','total_amt','address','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display=('invoice_no','item','image_tag','qty')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


#product review
class ProductReviewAdmin(admin.ModelAdmin):
    list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)



class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)