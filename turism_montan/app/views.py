from django.db.models import Avg, Value, FloatField, Count
from django.db.models.functions import Coalesce

from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test 

from django.contrib import messages

from .models import ZonaMontana, Traseu, ImagineTraseu, PunctDeInteres, Marcaj, Recenzie
from .forms import RegisterForm, TraseuForm, MarcajForm, ZonaMontanaForm, PuncteDeInteresForm, RecenzieForm

# REGISTER
def register_request(request):
    if request.method == "POST":
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inregistrare reusita!")
            return redirect("homepage")
        else:
            messages.error(request, "Inregistrare esuata. Verifica erorile de mai jos.")
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})

# LOGIN
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Te-ai logat ca {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Nume sau parola invalida.")
        else:
            messages.error(request, "Nume sau parola invalida.")
    else:
        form = AuthenticationForm()
        
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder'] = field.label

    return render(request, "app/login.html", {"form": form})

# LOGOUT
def logout_request(request):
    logout(request)
    messages.info(request, "Te-ai delogat cu succes.")
    return redirect("homepage")

# LEAGA TRASEU (PARINTELE) DE IMAGINI (COPILUL)
ImagineFormSet = inlineformset_factory(
    Traseu, 
    ImagineTraseu, 
    fields=('imagine',), 
    extra=1,
    can_delete=True
)

# LISTA TRASEE
def lista_trasee(request):
    zone = ZonaMontana.objects.all()
    zona_id_selectata = request.GET.get('zona')

    if zona_id_selectata:
        trasee = Traseu.objects.filter(zona__id=zona_id_selectata)
    else:
        trasee = Traseu.objects.all()
    
    trasee = trasee.order_by('-id')

    context = {
        'trasee': trasee,
        'zone': zone,
        'zona_activa': int(zona_id_selectata) if zona_id_selectata else None
    }

    return render(request, 'app/lista_trasee.html', context)

# DETALII TRASEU
def detalii_traseu(request, traseu_id):
    traseu = get_object_or_404(Traseu, id=traseu_id)
    recenzii = traseu.recenzii.all().order_by('-data_postarii')

    medie_note = recenzii.aggregate(Avg('evaluare'))['evaluare__avg']
    if request.method == 'POST' and request.user.is_authenticated:
        form = RecenzieForm(request.POST)
        if form.is_valid():
            recenzie_noua = form.save(commit=False)
            recenzie_noua.traseu = traseu
            recenzie_noua.user = request.user
            recenzie_noua.save()
            messages.success(request, "Recenzia ta a fost adaugata!")
            return redirect('detalii_traseu', traseu_id=traseu.id)
    else:
        form = RecenzieForm()
    context = {
        'traseu': traseu,
        'recenzii': recenzii,
        'medie_note': medie_note,
        'form': form,
    }
    return render(request, 'app/traseu.html', context)

def is_admin(user):
    return user.is_superuser

# AFISARE LISTA UTILIZATORI
@user_passes_test(is_admin)
def lista_utilizatori(request):
    users = User.objects.annotate(nr_recenzii=Count('recenzie')).order_by('-date_joined')
    return render(request, 'app/gestionare_utilizatori.html', {'users': users})

# STERGERE UTILIZATOR
@user_passes_test(is_admin)
def sterge_utilizator(request, user_id):
    user_de_sters = get_object_or_404(User, id=user_id)
    
    if user_de_sters == request.user:
        messages.error(request, "Nu iti poti sterge propriul cont!")
        return redirect('lista_utilizatori')
        
    user_de_sters.delete()
    messages.success(request, f"Utilizatorul {user_de_sters.username} a fost sters.")
    return redirect('lista_utilizatori')

# SCHIMBARE ROL UTILIZATOR
@user_passes_test(is_admin)
def schimba_rol(request, user_id):
    user_edit = get_object_or_404(User, id=user_id)
    
    if user_edit == request.user:
        messages.error(request, "Nu iti poti modifica propriul rol!")
        return redirect('lista_utilizatori')
    
    if user_edit.is_superuser:
        user_edit.is_superuser = False
        user_edit.is_staff = False
        messages.info(request, f"{user_edit.username} este acum un utilizator normal.")
    else:
        user_edit.is_superuser = True
        user_edit.is_staff = True
        messages.success(request, f"{user_edit.username} este acum Administrator.")
        
    user_edit.save()
    return redirect('lista_utilizatori')

# AFISARE RECENZII UTILIZATOR
@user_passes_test(is_admin)
def recenzii_user(request, user_id):
    user_vizat = get_object_or_404(User, id=user_id)
    recenzii = user_vizat.recenzie.all().order_by('-data_postarii')
    
    return render(request, 'app/recenzii_user.html', {
        'user_vizat': user_vizat,
        'recenzii': recenzii
    })

# ADAUGARE TRASEU
@user_passes_test(is_admin)
def adaugare_traseu(request):
    if request.method == 'POST':
        form = TraseuForm(request.POST, request.FILES)
        
        if form.is_valid():
            traseu_nou = form.save()
       
            formset = ImagineFormSet(request.POST, request.FILES, instance=traseu_nou)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Traseul si imaginile au fost adaugate.")
                return redirect('homepage')
    else:
        form = TraseuForm()
        formset = ImagineFormSet() 

    return render(request, 'app/formular_traseu.html', {
        'form': form, 
        'formset': formset,
        'titlu': 'Adauga Traseu Nou'
    })

# EDITARE TRASEU
@user_passes_test(is_admin)
def editare_traseu(request, traseu_id):
    traseu = get_object_or_404(Traseu, id=traseu_id)
    
    if request.method == 'POST':
        form = TraseuForm(request.POST, request.FILES, instance=traseu)
        formset = ImagineFormSet(request.POST, request.FILES, instance=traseu)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Traseul {traseu.nume_traseu} a fost actualizat!")
            return redirect('homepage')
    else:
        form = TraseuForm(instance=traseu)
        formset = ImagineFormSet(instance=traseu) 
    return render(request, 'app/formular_traseu.html', {
        'form': form, 
        'formset': formset,
        'titlu': f'Editeaza: {traseu.nume_traseu}'
    })

# ADAUGARE ZONA
@user_passes_test(is_admin)
def adaugare_zona(request):
    if request.method == 'POST':
        form = ZonaMontanaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona Montana a fost adaugata!")
            return redirect('homepage')
    else:
        form = ZonaMontanaForm()
    
    return render(request, 'app/formular_general.html', {
        'form': form, 
        'titlu': 'Adauga Zona Montana'
    })

# ADAUGARE MARCAJ
@user_passes_test(is_admin)
def adaugare_marcaj(request):
    if request.method == 'POST':
        form = MarcajForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Marcajul a fost adaugat!")
            return redirect('homepage')
    else:
        form = MarcajForm()
    
    return render(request, 'app/formular_general.html', {
        'form': form, 
        'titlu': 'Adauga Marcaj Nou'
    })

# ADAUGARE PUNCT DE INTERES
@user_passes_test(is_admin)
def adaugare_punct_interes(request):
    if request.method == 'POST':
        form = PuncteDeInteresForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Punctul de interes a fost adaugat!")
            return redirect('homepage')
    else:
        form = PuncteDeInteresForm()
    
    return render(request, 'app/formular_general.html', {
        'form': form, 
        'titlu': 'Adauga Punct de Interes'
    })

# HOMEPAGE
def homepage(request):
    zone = ZonaMontana.objects.all()
    trasee_recente = Traseu.objects.all().order_by('-id')[:6]
    trasee_hero = Traseu.objects.annotate(
        medie_stele=Coalesce(Avg('recenzii__evaluare'), Value(0),  output_field=FloatField())
    ).order_by('-medie_stele')[:3]
    
    context = {
        'zone': zone,
        'trasee': trasee_recente,
        'trasee_hero': trasee_hero,
    }
    return render(request, 'app/index.html', context) 