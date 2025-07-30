from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Product

from .forms import CommentForm


@require_POST
@login_required(login_url='/users/login')
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
                return render(request, 'main/partial/comments_list.html', {'comments': comments})

    return redirect('main:product_detail', id=product_id, slug=product_slug)
