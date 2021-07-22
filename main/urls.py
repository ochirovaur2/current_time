from django.urls import path
from . import views 

urlpatterns = [
    
    path('v1/get_current_time/', views.get_current_time, name='get_current_time')
]
