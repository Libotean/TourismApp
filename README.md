Pentru a rula acest proiect, asigura-te ca ai instalate:
1.  **Python** (v3.10 sau mai nou)
2.  **XAMPP**
3.  **Git**

---

## Ghid de Instalare si Configurare

Urmeaza acesti pasi pentru a rula aplicatia local:

### 1. Clonarea proiectului
Deschide terminalul si descarca proiectul:

```bash
git clone https://github.com/Libotean/TourismApp
cd turism_montan
```
### 2. Instalarea dependentelor

Instaleaza librariile necesare:

```bash
pip install -r requirements.txt
```

### 3. Configurarea Bazei de Date

  Deschide XAMPP Control Panel si porneste modulele Apache si MySQL.

  Deschide browserul si mergi la http://localhost/phpmyadmin.

  Fa click pe tab-ul SQL si ruleaza comanda:
  
```SQL
CREATE DATABASE turism_montan;
```

Deschide fisierul turism_montan/settings.py din proiect.

Cauta sectiunea DATABASES si completeaza datele tale.
```Python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'turism_montan',
            'USER': 'root',
            'PASSWORD': '',  
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
```

### 4. Initializarea si Importul Datelor
```bash
python manage.py migrate
```
```bash
python manage.py loaddata date_proiect.json
```
daca nu functioneaza foloseste
```bash
python -Xutf8 manage.py loaddata date_proiect.json
```
### 5. Pornirea Serverului Django
```bash
python manage.py runserver
```
Conturi de Acces (Logare)

Administrator:	admin	parola123

Utilizator: Test	parolaTest.	
