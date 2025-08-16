from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser


class Register(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class Login(FormView):
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


@login_required
def profile(request):
    user = request.user
    orders = user.orders.all()
    return render(request, 'users/profile.html', {'user': user, 'orders': orders})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {
        'user': request.user,
        'edit_mode': False,
    })


@login_required
def edit_profile_details(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('users:profile')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении профиля: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'form': form,
        'edit_mode': True
    })


@login_required
def update_account_details(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()
            user.save()
        else:
            form = CustomUserUpdateForm()
    return render(request, 'users/profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('main:product_list')
