from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Comment
from main.models import Product
from .forms import CommentForm


@login_required
def add_comment(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()

            if request.htmx:
                comments = product.comments.all().order_by('-created_at')
                return render(request, 'main/product/comments_list.html', {'comments': comments})

    return redirect('main:product_detail', id=product_id, slug=product_slug)
