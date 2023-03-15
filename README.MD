# Proyecto Gestor de Salas

## Requisitos para ejecutar en "Dev mode"

### Docker

Para ejecutar el proyecto abra la terminal y escriba `docker compose up`, asegurese de que el motor de docker esté en ejecución

Cuando esté en ejecución ejecute el siguiente comando `docker compose exec backend python manage.py migrate` para realizar las migraciones a la base de datos

### Ambiente local

**Backend**

Para ejecutar el proyecto, abra una terminal y asegurese de tener un ambiente virtual de `python3` ya sea en Windows, Linux o Mac

Luego muevase a la carpeta `src/backend/` y escriba en la terminal `pip install -r requirements.txt`

Finalmente, ejecute el proyecto escribiendo `python manage.py migrate` para generar las migraciones de la base de datos y `python manage.py runserver 0:8000` para que el proyecto comience a ejecutarse

## Primera ejecución

Una vez lenvantado el proyecto dirijase al sitio `127.0.0.1:8000` y encontrará el sitio inicial de instalación, siga las instrucciones

## Requisitos para ejecutar en "Production"

Dependiendo si usa **Docker**, **CI/CD con Kubernetes** o ejecuta el proyecto de manera tradicional usando algún servidor web como **Nginx** asegurese de configurar las siguientes variables de entorno:

``` config
# Django secret key
DJANGO_SECRET="secret key" # Se debe generar la llave para el backend de Django

# App name
APPNAME="Name" # Nombre del servicio

# URL HOST
URL_HOST="www.example.com" # Dominio donde se alojará el servicio

# Debugger
DEBUG=Bool # El proyecto está automáticamente configurado para trabajar en modo DEBUG=True por lo que se debe especificar False para que funcione en producción

# Deploy method
HEROKU_DEPLOY=Bool # True o False dependiendo si se ejecutará con Heroku container, si es falso o no se específica, el proyecto automaticamente se ejecutará funcionará con deploy tradicional o docker/kubernetes

# Email config
EMAIL_HOST = "smtp.example.com" # URL smtp del servicio de correo
EMAIL_USE_TLS = Bool # True o False si usa TLS
EMAIL_PORT = 0 # Número del puerto de servicio
EMAIL_HOST_USER = "username" # Nombre de usuario del servicio de correo
EMAIL_HOST_PASSWORD = "password" # Contraseña del servicio de correo

# Database config
HOST="db.example.com" # URL del host de la base de datos
NAME="example" # Nombre de la base de datos
USER="username" # Nombre de usuario de la base de datos
PASSWORD="password" # Contraseña de la base de datos

```
