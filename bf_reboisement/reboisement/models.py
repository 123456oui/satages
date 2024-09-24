from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils import timezone


# Create your models here.
class TypePlante(models.Model):
    id = models.AutoField(primary_key=True)
    type_plante = models.CharField(max_length=100)

    def __str__(self):
        return self.type_plante
    
class Plante(models.Model):
    id = models.AutoField(primary_key=True)
    nom_courant = models.CharField(max_length=100)
    nom_scientifique = models.CharField(max_length=100)
    type = models.ForeignKey(TypePlante, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nom_courant
    
class Acteur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mdp = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom} {self.email}"
    
class TypeStructure(models.Model):
    id = models.AutoField(primary_key=True)
    type_structure = models.CharField(max_length=100)

    def __str__(self):
        return self.type_structure
    
class Structure(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mail = models.EmailField(unique=True)
    logo = models.ImageField(upload_to='media/')
    type = models.ForeignKey(TypeStructure, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nom
    
class PersonnelStructure(models.Model):
    id = models.AutoField(primary_key=True)
    structure = models.ForeignKey(Structure, on_delete=models.DO_NOTHING)
    acteur = models.ForeignKey(Acteur, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.acteur} - {self.structure}"
    
class Partenaire(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    mail = models.EmailField(unique=True)

    def __str__(self):
        return self.nom
    
class TypeLocalite(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type
    
class Localite(models.Model):
    id = models.AutoField(primary_key=True)
    nom_localite = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    centrage = gis_models.PointField()
    type = models.ForeignKey(TypeLocalite, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nom_localite
    
class LocalitePolygone(models.Model):
    id = models.AutoField(primary_key=True)
    localite = models.ForeignKey(Localite, on_delete=models.DO_NOTHING)
    geom = gis_models.MultiPolygonField()

    def __str__(self):
        return f"Polygone de {self.localite.nom_localite}"
    
class Materiel(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
    
class Infos(models.Model):
    info = models.TextField()
    cree_le = models.DateTimeField(auto_now_add=True)
    modifier_le = models.DateTimeField(auto_now=True)
    valable_jusque= models.DateTimeField()

    def __str__(self):
        return self.info[:50]  # Affiche les 50 premiers caractères de l'info

class Carousel(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

    class Meta:
        ordering = ['order']
        
class Activite(models.Model):
    id = models.AutoField(primary_key=True)
    acteur = models.ForeignKey(Acteur, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    nb_plante = models.IntegerField()
    nb_participant = models.IntegerField()
    creer_le = models.DateTimeField(auto_now_add=True)
    modifier_le = models.DateTimeField(auto_now=True)
    statut = models.BooleanField(default=False)

    def a_eu_lieu(self):
        self.statut = True
        self.save()

    def est_annule(self):
        return self.date < timezone.now() and not self.statut

    def __str__(self):
        return f"Activité de {self.acteur} le {self.date}"
    
class SourceFinance(models.Model):
    id = models.AutoField(primary_key=True)
    partenaire = models.ForeignKey(Partenaire, on_delete=models.DO_NOTHING)
    activite = models.ForeignKey(Activite, on_delete=models.DO_NOTHING)
    montant = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Source de financement de {self.partenaire} pour {self.activite} pour un montant de {self.montant}"
    
class Plants(models.Model):
    id = models.AutoField(primary_key=True)
    plante = models.ForeignKey(Plante, on_delete=models.DO_NOTHING)
    activite = models.ForeignKey(Activite, on_delete=models.DO_NOTHING)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.plante.nom} pour {self.activite}"
    
class Media(models.Model):
    id = models.AutoField(primary_key=True)
    activite = models.ForeignKey(Activite, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='media/')
    creer_le = models.DateTimeField(auto_now_add=True)
    modifier_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Media pour {self.activite}"

    def save(self, *args, **kwargs):
        # Vérifie que le fichier est une vidéo ou une photo avant de sauvegarder
        if not self.file.name.lower().endswith(('.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png')):
            raise ValueError("Le fichier doit être une vidéo ou une photo.")
        super().save(*args, **kwargs)
        
class ActiviteMateriel(models.Model):
    id = models.AutoField(primary_key=True)
    activite = models.ForeignKey(Activite, on_delete=models.DO_NOTHING)
    materiel = models.ForeignKey(Materiel, on_delete=models.DO_NOTHING)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.materiel.nom} pour {self.activite}"
    
class Site(models.Model):
    id = models.AutoField(primary_key=True)
    polygone = gis_models.PolygonField()
    centrage = gis_models.PointField()
    localite = models.ForeignKey(Localite, on_delete=models.DO_NOTHING)
    activite = models.ForeignKey(Activite, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Site de {self.localite.nom_localite} pour {self.activite}"
