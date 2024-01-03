from django.urls import path
from .views import get_dynamics_data, create_dynamics_data, delete_dynamics_data,update_dynamics_data

urlpatterns = [
    path('get-dynamics-data/', get_dynamics_data, name='get_dynamics_data'),
    path('create-dynamics-data/', create_dynamics_data, name='create_dynamics_data'),
    path('delete-dynamics-data/<str:dataAreaId>/<str:CarId>/', delete_dynamics_data, name='delete_dynamics_data'), 
    path('update-dynamics-data/<str:dataAreaId>/<str:CarId>/', update_dynamics_data, name='update_dynamics_data'), 
]
