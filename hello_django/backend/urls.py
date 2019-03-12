from django.urls import path

from hello_django.backend import views

urlpatterns = [
    path('profile/', views.to_profile, name='url-backend-profile'),
    path('users/', views.to_users, name='url-backend-users'),
    path('roles/', views.to_roles, name='url-backend-roles'),
    path('menus/', views.to_menus, name='url-backend-menus'),

    path('ajax/user/page/', views.ajax_obtain_page_users, name='url-backend-ajax-user-page'),
    path('ajax/user/add/', views.ajax_add_user, name='url-backend-ajax-user-add'),
    path('ajax/user/update/', views.ajax_update_user, name='url-backend-ajax-user-update'),
    path('ajax/user/obtain/', views.ajax_obtain_user, name='url-backend-ajax-user-obtain'),

    path('ajax/role/page/', views.ajax_obtain_page_roles, name='url-backend-ajax-role-page'),
    path('ajax/role/all/', views.ajax_obtain_all_roles, name='url-backend-ajax-role-all'),
    path('ajax/role/add/', views.ajax_add_role, name='url-backend-ajax-role-add'),
    path('ajax/role/update/', views.ajax_update_role, name='url-backend-ajax-role-update'),
    path('ajax/role/obtain/', views.ajax_obtain_role, name='url-backend-ajax-role-obtain'),

    path('ajax/menu/page/', views.ajax_obtain_page_menus, name='url-backend-ajax-menu-page'),
    path('ajax/menu/all/', views.ajax_obtain_all_menus, name='url-backend-ajax-menu-all'),
    path('ajax/menu/add/', views.ajax_add_menu, name='url-backend-ajax-menu-add'),
    path('ajax/menu/update/', views.ajax_update_menu, name='url-backend-ajax-menu-update'),
    path('ajax/menu/obtain/', views.ajax_obtain_menu, name='url-backend-ajax-menu-obtain'),
]
