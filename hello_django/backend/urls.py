from django.urls import path
from hello_django.backend import views

urlpatterns = [
    path('profile/', views.to_profile, name='url-backend-profile'),
    path('users/', views.to_users, name='url-backend-users'),
    path('roles/', views.to_roles, name='url-backend-roles'),
    path('menus/', views.to_menus, name='url-backend-menus'),
    path('ajax/users/', views.ajax_obtain_users, name='url-backend-ajax-users'),
    path('ajax/roles/', views.ajax_obtain_roles, name='url-backend-ajax-roles'),
    path('ajax/menus/', views.ajax_obtain_menus, name='url-backend-ajax-menus'),
]
