from django.urls import path, include
from . import views
from online_car_sell_buy.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('car_seller', views.seller, name= 'car-seller'),
    path('update/<int:car_id>', views.update_car),
    path('delete/<int:car_id>', views.delete_car),
    path("accounts/", include("django.contrib.auth.urls"), name='login')
    
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)