from django.conf.urls import url 
from . import views 

urlpatterns = [
    url(r'^textinput', views.textinput, name='textinput'),
    url(r'^featureoutput', views.featureoutput, name='featureoutput'),
    url(r'^account', views.account, name='account'),
]


