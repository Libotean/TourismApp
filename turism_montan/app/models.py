from django.db import models
from django.contrib.auth.models import User

class ZonaMontana(models.Model):
    nume_zona = models.CharField(max_length=100, unique=True)
    regiune = models.CharField(max_length=100, blank=True, null=True)
    descriere = models.TextField(blank=True, null=True)
    imagine_reprezentativa = models.ImageField(upload_to='zone_montane/', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Zone Montane"
    def __str__(self):
        return self.nume_zona

class Marcaj(models.Model):
    TIPURI = [('banda', 'Banda'), ('cruce', 'Cruce'), ('triunghi', 'Triunghi'), ('punct', 'Punct/Cerc')]
    CULORI = [('rosu', 'Rosu'), ('galben', 'Galben'), ('albastru', 'Albastru')]
    tip = models.CharField(max_length=10, choices=TIPURI)
    culoare = models.CharField(max_length=10, choices=CULORI)
    imagine = models.ImageField(upload_to='marcaje_icons/', blank=True, null=True)
    class Meta:
        verbose_name_plural = "Marcaje"
        unique_together = ('tip', 'culoare')
    def __str__(self):
        return f"{self.get_tip_display()} {self.get_culoare_display()}"

class PunctDeInteres(models.Model):
    TIPURI = [('cabana', 'Cabana'), ('lac', 'Lac'), ('cascada', 'Cascada'), ('varf', 'Varf'), ('refugiu', 'Refugiu')]
    nume_pct = models.CharField(max_length=150)
    tip_pct = models.CharField(max_length=10, choices=TIPURI)
    zona = models.ForeignKey(ZonaMontana, on_delete=models.CASCADE)
    descriere = models.TextField(blank=True, null=True)
    latitudine = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitudine = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    imagine = models.ImageField(upload_to='puncte_interes/', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Puncte de Interes"
    def __str__(self):
        return self.nume_pct

class Traseu(models.Model):
    DIFICULTATE = [('usor', 'Usor'), ('mediu', 'Mediu'), ('dificil', 'Dificil'), ('expert', 'Expert')]
    SEZON = [('primavara', 'Primavara'), ('vara', 'Vara'), ('toamna', 'Toamna'), ('iarna', 'Iarna'), ('tot_timpul', 'Tot timpul')]
    nume_traseu = models.CharField(max_length=150)
    zona = models.ForeignKey(ZonaMontana, on_delete=models.CASCADE)
    marcaje = models.ManyToManyField(Marcaj, related_name='trasee')
    dificultate = models.CharField(max_length=10, choices=DIFICULTATE)
    durata_traseu = models.DecimalField(max_digits=4, decimal_places=1)
    distanta_km = models.DecimalField(max_digits=5, decimal_places=1)
    altitudine_maxima = models.IntegerField(null=True, blank=True)
    sezon_recomandat = models.CharField(
        max_length=20, 
        choices=SEZON, 
        null=True, 
        blank=True
    )
    descriere = models.TextField(blank=True, null=True)
    track_gpx = models.FileField(upload_to='trasee_gpx/', null=True, blank=True)
    puncte_interes = models.ManyToManyField(PunctDeInteres, blank=True)
    class Meta:
        verbose_name_plural = "Trasee"
    def __str__(self):
        return self.nume_traseu

class ImagineTraseu(models.Model):
    traseu = models.ForeignKey(Traseu, related_name='imagini', on_delete=models.CASCADE)
    imagine = models.ImageField(upload_to='trasee_foto/')
    descriere = models.CharField(max_length=100, blank=True, null=True)

class Recenzie(models.Model):
    traseu = models.ForeignKey(Traseu, related_name='recenzii', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recenzie')
    evaluare = models.IntegerField(choices=[(i, f'{i} Stele') for i in range(1, 6)])
    comentariu = models.TextField()
    data_postarii = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Recenzii"