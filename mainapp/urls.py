from django.urls import path, include

from mainapp import views

urlpatterns = [
    path('',views.stockPicker, name='stockPicker'),
    path('stocktracker/',views.stockTracker, name='stockTracker'),
]