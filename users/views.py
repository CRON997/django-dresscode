from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
        else:
            messages.error(request, 'Ошибка входа в систему')
            print("Form errors:", form.errors)  # Для отладки
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'users/profile.html', {'user': user})


@login_required
@login_required
def profile_view(request):
    """Отображение профиля пользователя"""
    return render(request, 'users/profile.html', {
        'user': request.user,
        'edit_mode': False
    })


@login_required
def edit_profile_details(request):
    """Редактирование профиля пользователя"""
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
