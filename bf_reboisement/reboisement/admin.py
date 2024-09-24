from django.contrib import admin
from .models import *
from django.contrib.gis import admin as gis_admin
from django.contrib.gis import admin as gis_admin
from django.contrib.gis.db import models as gis_models


# Enregistrement des modèles dans l'admin
@admin.register(TypePlante)
class TypePlanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_plante')  # Colonnes affichées dans la liste
    search_fields = ('type_plante',)  # Champs de recherche


@admin.register(TypeStructure)
class TypeStructureAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_structure')
    search_fields = ('type_structure',)


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'mail')
    search_fields = ('nom', 'mail')


@admin.register(TypeLocalite)
class TypeLocaliteAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type',)


@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')
    search_fields = ('title',)
    list_editable = ('order',)  # Permet d'éditer directement l'ordre dans la liste
    ordering = ('order',)  # Tri par l'ordre spécifié

@admin.register(Plante)
class PlanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_courant','nom_scientifique')  # Colonnes affichées dans la liste
    search_fields = ('nom_courant',)  # Champs de recherche

@admin.register(Acteur)
class ActeurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom','prenom','email')  # Colonnes affichées dans la liste
    search_fields = ('email',)  # Champs de recherche
@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'date','acteur','nb_plante','nb_participant')  # Colonnes affichées dans la liste
    search_fields = ('id',)  # Champs de recherche
    
class LocaliteAdmin(gis_admin.GISModelAdmin):
    list_display = ('nom_localite', 'centrage', 'type')
    search_fields = ('nom_localite',)
    list_filter = ('type',)

class SiteAdmin(gis_admin.GISModelAdmin):
    list_display = ('localite', 'activite', 'centrage')
    search_fields = ('localite__nom_localite', 'activite__nom',)
    list_filter = ('localite', 'activite')

admin.site.register(Localite, LocaliteAdmin)
admin.site.register(Site, SiteAdmin)

admin.site.register(SourceFinance)
admin.site.register(Structure)
@admin.register(PersonnelStructure)
class PersonnelStructureAdmin(admin.ModelAdmin):
    list_display = ('acteur', 'structure')