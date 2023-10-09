from django.urls import path
from .views import post, put, get, delete
app_name = "polls"
urlpatterns = [
    path('post/<str:process>/<str:action>', post, name='post'),
    path('put/<str:process>/<str:action>/<str:id>', put, name='put'),
    path('get/<str:process>/<str:action>/<str:id>', get, name='get'),
    path('delete/<str:process>/<str:action>/<str:id>', delete, name='delete'),
]
