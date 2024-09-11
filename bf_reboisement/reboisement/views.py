from django.shortcuts import render

# Create your views here.
def acceuil(request):
    return render(request, 'index.html')

def admin(request):
    return render(request, 'acceuil.html')