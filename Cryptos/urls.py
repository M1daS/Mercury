from django.conf.urls import url, include
from . import views


urlpatterns = [


	url(r'^$', views.cryptoroot, name = 'cryptoroot'),
	url(r'^Correlate/$', views.correlate, name = 'correlate'),
	url(r'^BBStrat/$', views.bbstrat, name = 'bbstrat')


]