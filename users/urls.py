from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-details/', views.edit_profile_details, name='edit_profile_details'),
    path('update-details/', views.update_account_details, name='update_account_details')
]
