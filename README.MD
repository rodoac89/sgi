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
DEFAULT_DEPLOY="tipo de deploy" # se debe especificar si se va a desplegar en Heroku, Produccion o Desarrollo:

# Heroku: DEFAULT_DEPLOY="heroku"
# Producción(Tradicional o en contenedores): DEFAULT_DEPLOY="production"
# Desarrollo: No es necesario especificar esta variable

# Email config
EMAIL_HOST = "smtp.example.com" # URL smtp del servicio de correo
EMAIL_USE_TLS = Bool # True o False si usa TLS
EMAIL_PORT = 0 # Número del puerto de servicio
EMAIL_HOST_USER = "username" # Nombre de usuario del servicio de correo
EMAIL_HOST_PASSWORD = "password" # Contraseña del servicio de correo

# Database config (Solo para producción o heroku)
HOST="db.example.com" # URL del host de la base de datos
NAME="example" # Nombre de la base de datos
USER="username" # Nombre de usuario de la base de datos
PASSWORD="password" # Contraseña de la base de datos

```

## Instalación del servicio y aplicación Activity en Windows

### Contexto

Antes de todo se debe definir qué hacen estos dos programas:

Servicio Activity: Servicio de Windows que envía datos de uso del computador, incluyendo hora de encendido y apagado, además de enviar una señal de vida recurrentemente.

Aplicación de escritorio Activity: Aplicación de Windows que muestra una alerta de inactividad en el computador y que apagará el equipo después de un determinado tiempo si el usuario no cancela esta acción.

### Ahora sí instalación

Para instalar el Servicio Activity se debe ejecutar el instalador con extensión .msi e ingresar los datos solicitados, que son el dominio del servidor al que se enviarán los datos de uso y el secret que se utiliza en la conexión con el servidor mediante Websocket. Como requisito para que funcione correctamente el servicio, se debe desactivar la opción de inicio rápido en la configuración de energía de Windows.

Para instalar la Aplicación Activity se debe pegar el ejecutable con extensión .exe en la carpeta de inicio del usuario, para que se ejecute al iniciar sesión. Los pasos para hacer esto son:

1. Tener la sesión iniciada en el usuario en el que se quiera instalar, en este caso sería el usuario dedicado para estudiantes.
2. Pulsar las teclas Windows + R
3. Escribir shell:startup
4. En la ventana que se abre pegar el ejecutable ActivityApp.exe