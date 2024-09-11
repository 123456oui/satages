from django.urls import path
from . import views 


urlpatterns = [
    # Ajoute tes patterns d'URL ici
    path('', views.acceuil, name='home'),
    path('admine', views.admin, name='admin'),
    ]