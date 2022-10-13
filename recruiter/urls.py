from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="Home"),
    path('recruiter/', views.index, name="recruiter"),
    path('success/<int:id>', views.success, name="Success"), 
    path('decline/<int:id>', views.decline, name="Decline"), 
    path('contact/', views.contact, name="Contact"),
    path('response/<int:id>', views.response, name="Response"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
