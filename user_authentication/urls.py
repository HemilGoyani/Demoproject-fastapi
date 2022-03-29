from django.urls import path, include
from . import views
from online_car_sell_buy.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path("accounts/", include("django.contrib.auth.urls"), name='login'),
    path('registration/', views.registration, name='registration'),
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)