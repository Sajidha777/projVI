from django.shortcuts import render
from django.http import JsonResponse
from .models import Banner, Category,Brand, Product, ProductAttribute
from django.template.loader import render_to_string
# Create your views here.

#Home Page
def home(request):
    banners = Banner.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=True).order_by('-id')
    return render(request,'index.html',{'data':data,'banners':banners})


#Category-list
def  category_list(request):
    data=Category.objects.all().order_by('-id')
    return  render(request,'category_list.html',{'data':data})


#Brand-list
def brands_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})


#Product-list
def product_list(request):
    total_data=Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]
    return render(request,'product_list.html',
    {
        'data':data,
        'total_data': total_data,   
    })



#Product list according to category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')
    return render(request,'category_product_list.html',{'data':data})


#Product list accoriding to brand
def brand_product_list(request,brand_id):
    brand=Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    return render(request,'brand_product_list.html',{'data':data})


#Product Detail
def product_detail(request,slug,id):
    product=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    sizes=ProductAttribute.objects.filter(product=product).values('id','size__id','size__title','price','color__id','image').distinct()
    return render(request,'product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes})


#Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'search.html',{'data':data,})


#Filter Data
def filter_data(request):
    colors=request.GET.getlist('color[]')
    brands=request.GET.getlist('brand[]')
    categories=request.GET.getlist('category[]')
    sizes=request.GET.getlist('size[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts=Product.objects.all().order_by('-id')
    allProducts=allProducts.filter(productattribute__price__gte=minPrice).distinct()
    allProducts=allProducts.filter(productattribute__price__lte=maxPrice).distinct()
    if len(colors)>0:
        allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('ajax/product-list.html',{'data':allProducts})#to pass data as list ,pass thru template
    
    return JsonResponse({'data':t})



#Load More
def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t=render_to_string('ajax/product-list.html',{'data':data})
    return JsonResponse({'data':t})



#Add to Cart
def add_to_cart(request):
    #using session. cart items are saved in database only for logged in users. for others it's saved in sessions
    cart_p={}
    cart_p[str(request.GET['id'])]={
        'image':request.GET['image'],
        'prodid':request.GET['prodid'],
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_data[str(request.GET['id'])]['qty'])+int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})


# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt},)
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})

    

#Delete cart item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})

	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


#Update Cart Item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})



#Sign up
def signup(request):
    return