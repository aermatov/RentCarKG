from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('marks/', views.CarMarkListAPIView.as_view(), name='mark-list'),
    path('bodies/', views.CarBodyListAPIView.as_view(), name='body-list'),
    path('models/', views.CarModelListAPIView.as_view(), name='model-list'),
    path('fuel-types/', views.FuelTypeListAPIView.as_view(), name='fuel-type-list'),
    path('colors/', views.CarColorListAPIView.as_view(), name='color-list'),

    path('cars/', views.CarListAPIView.as_view(), name='car-list'),
    path('cars/<int:pk>/', views.CarDetailAPIView.as_view(), name='car-detail'),
    path('cars/create/', views.CarCreateAPIView.as_view(), name='car-create'),
    path('cars/<int:pk>/update/', views.CarUpdateAPIView.as_view(), name='car-update'),
    path('cars/<int:pk>/delete/', views.CarDeleteAPIView.as_view(), name='car-delete'),
    path('cars/<int:pk>/similar/', views.car_similar, name='car-similar'),

    path('car-images/create/', views.CarImageCreateAPIView.as_view(), name='car-image-create'),
    path('car-images/<int:pk>/delete/', views.CarImageDeleteAPIView.as_view(), name='car-image-delete'),

    path('rents/', views.RentListAPIView.as_view(), name='rent-list'),
    path('rents/<int:pk>/', views.RentDetailAPIView.as_view(), name='rent-detail'),
    path('rents/create/', views.RentCreateAPIView.as_view(), name='rent-create'),
    path('rents/<int:pk>/update/', views.RentUpdateAPIView.as_view(), name='rent-update'),
    path('rents/<int:pk>/delete/', views.RentDeleteAPIView.as_view(), name='rent-delete'),
    path('rents/check-availability/', views.rent_check_availability, name='rent-check-availability'),
]
