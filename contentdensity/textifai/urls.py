from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^textinput/$', views.textinput, name='textinput'),
    url(r'^featureoutput/(?P<pk>[-\w]+$)', views.featureoutput, name='featureoutput'),
    url(r'^account', views.account, name='account'),
    url(r'^general-insights$', views.general_insights, name='general-insights'),
    url(r'^texts$', views.allTexts, name='text-list'),
    url(r'^searchresults/(?P<query>.*$)', views.searchresults, name='searchresults'),
]
