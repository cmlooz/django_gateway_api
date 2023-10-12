from django.urls import path
from .views import post, put, get, delete
app_name = "polls"
urlpatterns = [
    path('<str:process>/<str:action>', post, name='post'),
    path('<str:process>/<str:action>/<str:id>', put, name='put'),
    path('<str:process>/<str:action>/<str:id>', get, name='get'),
    path('<str:process>/<str:action>/<str:id>', delete, name='delete'),
]
