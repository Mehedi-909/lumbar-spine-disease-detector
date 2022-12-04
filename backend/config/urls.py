from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path
from django.contrib import admin
from django.urls import path, include
from deep_learning import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dl/', views.image_processing),
    path('input/', views.get_image),
    #path('predictImage/',views.predictImage),
    path('predictImage/',views.crop_image),
    path('viewDataBase/',views.viewDataBase),
    path('api/', include('classifier.urls')),
    path('get_data/', views.get_data, name='get_data'),
    path('report/', views.report, name='report'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
