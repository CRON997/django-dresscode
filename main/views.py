from django.shortcuts import render,get_object_or_404
from main.models import Category, Product

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # category = None
    # if category_slug:
    #     category = get_object_or_404(Category,category_slug=category_slug)
    #     products = products.filter(category=category)

    context = {'categories':categories,'products':products}

    return render(request,'main/product/catalog.html',context)


def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    context = {'product':product}

    return render(request,'main/product/detail.html',context)

def about(request):
    return render(request,'main/product/about.html')
