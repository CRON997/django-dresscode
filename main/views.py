from django.shortcuts import get_object_or_404, render

from comments.forms import CommentForm
from comments.models import Comment
from main.models import Category, Product, Size


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {'categories': categories, 'products': products, 'category': category}

    if request.htmx:
        return render(request, 'main/partial/product_list_partial.html', context)

    return render(request, 'main/catalog.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = Comment.objects.filter(product=product)
    form = CommentForm()
    sizes = Size.objects.filter(productsize__product=product)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    context = {'product': product, 'comments': comments, 'related_products': related_products, 'form': form,
               'sizes': sizes}

    return render(request, 'main/detail.html', context)


def about(request):
    return render(request, 'main/about.html')
