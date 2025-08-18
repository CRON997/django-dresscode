from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from apps.comments.forms import CommentForm
from apps.comments.models import Comment
from apps.main.models import Category, Product, Size, Brand


class CatalogView(ListView):
    model = Product
    template_name = 'main/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.available_products.filter(available=True).select_related('category')
        category_slug = self.kwargs.get('category_slug')
        sort_option = self.request.GET.get('sort', 'name')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        in_stock = self.request.GET.get('stock')
        brands = self.request.GET.getlist('brands')

        print(sort_option)
        print(min_price)
        print(max_price)
        print(in_stock)
        print(brands)

        if sort_option == 'name_desc':
            products = Product.objects.all().order_by('-name').select_related('category')
        elif sort_option == 'price_asc':
            products = Product.objects.all().order_by('price').select_related('category')
        elif sort_option == 'price_desc':
            products = Product.objects.all().order_by('-price').select_related('category')

        if brands:
            products = Product.objects.filter(brand__in=brands)

        if min_price and max_price:
            products = Product.objects.filter(price__lte=max_price, price__gte=min_price)

        if in_stock == 'on-sale':
            products = Product.objects.filter(status_discount=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().values('name')
        context['current_sort'] = self.request.GET.get('sort', 'featured')
        context['brands'] = Brand.objects.all()
        return context

    # def get_template_names(self):
    #     if self.request.htmx:
    #         return ['product_list_partial.html']
    #     return ['catalog.html']


class Search(ListView):
    template_name = 'main/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = Comment.objects.filter(product=product)
    sizes = Size.objects.filter(productsize__product=product)
    related_products = Product.available_products.filter(category=product.category, available=True).exclude(
        id=product.id)[:4]

    form = CommentForm()

    context = {'product': product, 'comments': comments, 'related_products': related_products, 'form': form,
               'sizes': sizes}

    return render(request, 'main/detail.html', context)


def about(request):
    return render(request, 'main/about.html')
