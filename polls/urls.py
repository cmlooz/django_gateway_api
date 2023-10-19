from django.urls import path
# from .views import post, put, get, delete
from .views import handler
app_name = "polls"
urlpatterns = [
    path(r'<str:process>/<str:action>', handler, name='post'),
    path(r'<str:process>/<str:action>', handler, name='put'),
    path(r'<str:process>/<str:action>', handler, name='get'),
    path(r'<str:process>/<str:action>', handler, name='delete'),
]
