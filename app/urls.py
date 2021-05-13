from django.conf.urls import url
from django.urls import path
from app import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('eiou_claim/', views.EIOUClaimViews.as_view(), name='eiou_claim'),
    path('upload/', views.upload, name='upload'),

    ]
