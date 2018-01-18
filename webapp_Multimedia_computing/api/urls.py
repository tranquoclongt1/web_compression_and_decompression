from django.conf.urls import url

from . import views
from .views import  Multimedia_engine
urlpatterns = [
    url(r'^view$', Multimedia_engine.as_view(), name='multimedia-engine'),
    url('', views.index, name='index'),
]