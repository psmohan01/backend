from django.urls import path
from . import views
urlpatterns = [
    path('availability/', views.availability),
    path('create/', views.create_booking),
]
