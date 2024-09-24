from django.urls import path
from . import views 


urlpatterns = [
    # Ajoute tes patterns d'URL ici
    path('home', views.acceuil, name='home'),
    path('admine', views.admin, name='admine'),
    path('login', views.user_login, name='login'),
    path('get_activites', views.get_activites, name='get_activites'),
    path('details/<int:id>/', views.getdetails, name='getdetails'),
    path('get-polygones', views.get_polygones, name='get-polygones'), 
    path('add_or_update_structure', views.add_or_update_structure, name='add_or_update_structure'),
    path('delete_structure/<int:id>/', views.delete_structure, name='delete_structure'),
    path('load_types',views.load_types, name='load_types'),
    path('load_structures', views.load_structures, name='load_structures'), 
    path('load_users/', views.load_users, name='load_users'),
    path('add_or_update_user', views.add_or_update_user, name='add_or_update_user'),
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    ]