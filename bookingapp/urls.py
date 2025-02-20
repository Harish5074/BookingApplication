from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('book/', views.book_item, name='book_item'),
    path('cancel/', views.cancel_booking, name='cancel_booking'),
]
