from django.urls import path

from hello_django.backend import views

urlpatterns = [
    path('profile/', views.to_profile, name='url-backend-profile'),
    path('users/', views.to_users, name='url-backend-users'),
    path('roles/', views.to_roles, name='url-backend-roles'),
    path('menus/', views.to_menus, name='url-backend-menus'),
    path('ajax/page/users/', views.ajax_obtain_page_users, name='url-backend-ajax-page-users'),
    path('ajax/page/roles/', views.ajax_obtain_page_roles, name='url-backend-ajax-page-roles'),
    path('ajax/page/menus/', views.ajax_obtain_page_menus, name='url-backend-ajax-page-menus'),
    path('ajax/add/user/', views.ajax_add_user, name='url-backend-ajax-add-user'),
    path('ajax/update/user/', views.ajax_update_user, name='url-backend-ajax-update-user'),
    path('ajax/obtain/user/', views.ajax_obtain_user, name='url-backend-ajax-obtain-user'),
]
