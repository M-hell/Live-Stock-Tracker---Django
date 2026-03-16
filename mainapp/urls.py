from django.urls import path, include

from mainapp import views

urlpatterns = [
    path('',views.stockPicker, name='stockPicker'),
    path('asgiui/', views.asgiui, name='asgiui'),
    path('asgitrig/<str:trigger_id>/', views.asgitrig, name='asgitrig'),
]