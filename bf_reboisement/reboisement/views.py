from django.shortcuts import render
from .models import *
# Create your views here.
def acceuil(request):
    carousels = Carousel.objects.all() 
    # Récupérer les ID des acteurs associés à des structures
    acteurs_associés = PersonnelStructure.objects.values_list('acteur_id', flat=True)
    
    # Récupérer les ID des structures pour chaque type
    types_structure = ['ONG', 'ETATIQUE', 'ASSOCIATION']
    activites_par_type = {}

    for type_structure in types_structure:
        # Récupérer les ID des structures pour ce type
        structures = Structure.objects.filter(type__type_structure=type_structure)
        # Récupérer les ID des acteurs associés à ces structures
        acteurs_par_structure = PersonnelStructure.objects.filter(structure__in=structures).values_list('acteur_id', flat=True)
        # Récupérer les activités pour ces acteurs
        activites = Activite.objects.filter(acteur__in=acteurs_par_structure)
        activites_par_type[type_structure] = activites

    # Récupérer les activités des acteurs non associés à des structures
    activites_non_associées = Activite.objects.filter(acteur__in=Acteur.objects.exclude(id__in=acteurs_associés))

    # Récupérer les détails pour chaque activité
    activite_details = {}
    for activite in Activite.objects.all():
        # Sources de financement
        sources_financement = SourceFinance.objects.filter(activite=activite)
        # Structure
        structure = Structure.objects.filter(personnelstructure__acteur=activite.acteur).first()
        # Localité
        localite = Localite.objects.filter(site__activite=activite).first()
        # Médias
        medias = Media.objects.filter(activite=activite)
        # Matériels
        materiels = ActiviteMateriel.objects.filter(activite=activite)
        
        activite_details[activite.id] = {
            'sources_financement': sources_financement,
            'structure': structure,
            'localite': localite,
            'medias': medias,
            'materiels': materiels
        }

    context = {
        'activites_ONG': activites_par_type.get('ONG', []),
        'activites_ETATIQUE': activites_par_type.get('ETATIQUE', []),
        'activites_ASSOCIATION': activites_par_type.get('ASSOCIATION', []),
        'activites_non_associées': activites_non_associées,
        'activite_details': activite_details,
        'carousels': carousels
    }
    
    return render(request, 'index.html', context)

def admin(request):
    acteurs = Acteur.objects.all()
    nbacteur = acteurs.count()
    partenaires = Partenaire.objects.all()
    nbpartenaire = partenaires.count()
    localite=Localite.objects.all()
    nblocalite=localite.count()
    plante=Plante.objects.all()
    site=Site.objects.all()
    nbsite=site.count()
    activite=Activite.objects.all()
    nbactivite=activite.count()
    structure=Structure.objects.all()
    nbstructure=structure.count()
    context = { 'acteurs':acteurs, 'partenaires':partenaires,'localite':localite,'plante':plante, 'site':site,'activite':activite,'structure':structure,
               'nbsite':nbsite,'nbacteur':nbacteur, 'nbpartenaire':nbpartenaire,'nblocalite':nblocalite,'nbactivite':nbactivite,'nbstructure':nbstructure
               }
    
    return render(request, 'acceuil.html',context=context)




from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login  # Import correct
from .forms import UserForm  # Importation de ton formulaire personnalisé
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


def user_login(request):
    form = UserForm(request, data=request.POST or None)  # Utilise ton formulaire personnalisé
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authentifier l'utilisateur
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Si l'utilisateur est authentifié, démarrer la session
                auth_login(request, user)  # Utilisation de la fonction login importée comme auth_login
                
                # Rediriger vers la page d'accueil ou tableau de bord
                return redirect('admine')  # Remplacer 'admine' par l'URL de ta page cible
                
            else:
                # Si l'authentification échoue
                messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
        else:
            # Si le formulaire est invalide
            messages.error(request, 'Erreur dans le formulaire. Veuillez vérifier vos informations.')

    return render(request, 'login.html', {'form': form})


from django.http import JsonResponse

def get_activites(request):
    activites = Activite.objects.all()  # Récupérer toutes les activités
    activite_list = []
    for activite in activites:
        site = Site.objects.get(activite=activite)
        if activite.statut :
            sat="effectue"
        else:
            sat='en cours'
        activite_list.append({
            'id': activite.id,
            'date': activite.date.strftime('%d %B %Y, %H:%M'),
            'acteur': activite.acteur.nom + "  " + activite.acteur.prenom,  # Supposons que l'acteur ait un champ 'nom'
            'nb_plantes': activite.nb_plante,
            'nb_participants': activite.nb_participant,
            'localite': site.localite.nom_localite,  # Supposons que la localité ait un champ 'nom'
            'statut': sat,
        })

    return JsonResponse({'activites': activite_list})

from collections import defaultdict
import json

def getdetails(request, id):
    activite = get_object_or_404(Activite, id=id)
    site = Site.objects.select_related('localite').get(activite=activite)
    localite = site.localite
    sourcefinance = SourceFinance.objects.filter(activite=activite)
    
    revenue = defaultdict(int)
    total = 0
    for source in sourcefinance:
        revenue[source.partenaire.nom] += source.montant
        total += source.montant
    
    date_formatee = activite.date.strftime('%Y-%m-%dT%H:%M')  # Format pour datetime-local
    site_geojson = json.loads(site.polygone.geojson)  # Assurez-vous que c'est un dict
    
    acteur = activite.acteur 
    acc = "inexistant"
    if PersonnelStructure.objects.filter(acteur=acteur).exists():
        ac = PersonnelStructure.objects.get(acteur=acteur)
        acc = ac.structure.nom
    
    data = {
        'budget': total,
        'finance': dict(revenue),
        'site': site_geojson,  # Déjà un dict, pas besoin de le convertir en string
        'id': activite.id,
        'date': date_formatee,
        'acteur': f"{activite.acteur.nom} {activite.acteur.prenom}",
        'acteur_id': activite.acteur.id,
        'nb_plantes': activite.nb_plante,
        'nb_participants': activite.nb_participant,
        'localite': localite.nom_localite,
        'localite_id': localite.id,
        'date_modification': activite.modifier_le.strftime('%Y-%m-%dT%H:%M'),
        'structure': acc,
    }
    return JsonResponse(data)

def get_polygones(request):
    activites = Activite.objects.all()
    data = []
    
    for activite in activites:
        site = Site.objects.filter(activite=activite).first()
        if site:
            # Récupérer le centre et les coordonnées du polygone
            polygone = site.polygone
            coordinates = list(polygone.coords[0])  # Récupérer les coordonnées du polygone
            center = [polygone.centroid.y, polygone.centroid.x]  # Centrage du polygone
            
            data.append({
                'id': activite.id,
                'date': activite.date.strftime('%d %B %Y'),
                'acteur': f"{activite.acteur.nom} {activite.acteur.prenom}",
                'nb_plantes': activite.nb_plante,
                'nb_participants': activite.nb_participant,
                'coordinates': coordinates,
                'center': center
            })
    
    return JsonResponse(data, safe=False)

from django.views.decorators.http import require_POST

@require_POST
def add_or_update_structure(request):
    print(request.POST)
    if request.POST.get('id'):  # Si un ID est présent, nous modifions
        structure = Structure.objects.get(id=request.POST['id'])
        structure.nom = request.POST['nom']
        structure.mail = request.POST['mail']
        structure.logo = request.FILES.get('logo', structure.logo)  # Garde l'ancien logo s'il n'est pas changé
        structure.type_id = request.POST['type']
        structure.save()
    else:  # Ajout d'une nouvelle structure
        structure = Structure.objects.create(
            nom=request.POST['nom'],
            mail=request.POST['mail'],
            logo=request.FILES.get('logo'),
            type_id=request.POST['type']
        )
    
    return JsonResponse({'id': structure.id})

def delete_structure(request, id):
    structure = Structure.objects.get(id=id)
    structure.delete()
    return JsonResponse({'success': True})

def load_types(request):
    types = TypeStructure.objects.all()
    return JsonResponse({'types': list(types.values('id', 'type_structure'))})

def load_structures(request):
    structures = Structure.objects.select_related('type').all()
    
    # Construire la liste des structures avec leur type associé
    structure_list = []
    for structure in structures:
        structure_list.append({
            'id': structure.id,
            'nom': structure.nom,
            'mail': structure.mail,
            'logo': structure.logo.url if structure.logo else None,  # URL du logo ou None si pas de logo
            'type_structure': structure.type.type_structure  # Accéder au type lié
        })
    return JsonResponse({'structures': structure_list})


def load_users(request):
    users = User.objects.all()
    user_list = [{
        'id': user.id,
        'nom': user.first_name,
        'prenom': user.last_name,
        'mail': user.email,
        'password': user.password, 
    } for user in users]
    print(user_list)
    return JsonResponse({'users': user_list})

from django.contrib.auth.models import User
from django.http import JsonResponse

def add_or_update_user(request):
    if request.method == 'POST':
        
        user_id = request.POST.get('id')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('mail')
        password = request.POST.get('password')

        if user_id:  # Si un utilisateur existe, on le met à jour
            try:
                user = User.objects.get(pk=user_id)
                user.first_name = nom
                user.last_name = prenom
                user.email = email
                if password:  # Mettre à jour le mot de passe seulement s'il est fourni
                    user.set_password(password)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Utilisateur non trouvé.'}, status=404)
        else:  # Sinon on en crée un nouveau
            if not password:  # Vérifier qu'un mot de passe est fourni pour la création
                return JsonResponse({'error': 'Le mot de passe est requis pour la création.'}, status=400)
            
            user = User.objects.create(
                first_name=nom,
                last_name=prenom,
                email=email,
                username=email
            )
            user.set_password(password)  # Hacher le mot de passe

        user.save()
        return JsonResponse({'id': user.id})
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

    
    
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'})