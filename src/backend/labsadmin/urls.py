from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from apps.authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('apps.core.urls')),
    path('activity/', include('apps.activity.urls')),
    path('monitoring/', include('apps.monitoring.urls')),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('schedules/', include('apps.schedules.urls')),
    #path('licenses/', include(('apps.licenses.urls','licenses'))),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
