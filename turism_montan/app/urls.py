from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('traseu/adauga/', views.adaugare_traseu, name='adaugare_traseu'),
    path('traseu/editare/<int:traseu_id>/', views.editare_traseu, name='editare_traseu'),
    path('zona/adauga/', views.adaugare_zona, name='adaugare_zona'),
    path('marcaj/adauga/', views.adaugare_marcaj, name='adaugare_marcaj'),
    path('punct/adauga/', views.adaugare_punct_interes, name='adaugare_punct'),
    path('trasee/', views.lista_trasee, name='lista_trasee'),
    path('traseu/<int:traseu_id>/', views.detalii_traseu, name='detalii_traseu'),
    path('administrare/utilizatori/', views.lista_utilizatori, name='lista_utilizatori'),
    path('administrare/utilizatori/sterge/<int:user_id>/', views.sterge_utilizator, name='sterge_utilizator'),
    path('administrare/utilizatori/rol/<int:user_id>/', views.schimba_rol, name='schimba_rol'),
    path('administrare/utilizatori/recenzii/<int:user_id>/', views.recenzii_user, name='recenzii_user'),

]
