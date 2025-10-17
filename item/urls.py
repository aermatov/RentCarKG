from django.urls import path, include
from . import views
urlpatterns = [
    path('car-list/', views.CarListAPIView.as_view())
]