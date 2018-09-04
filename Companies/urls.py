from django.conf.urls import url, include
from . import views



'''
This Companies app rperesents basic/background information about each 
company. It is the PROFILE of the company
https://finance.yahoo.com/quote/NVDA/profile?p=NVDA
'''

urlpatterns = [
	#/Companies/
	url(r'^$', views.companies, name = 'companies'),
	url(r'^Watchlist/', views.watchlist, name = 'watchlist'),



	# #/Companies/123/
	# #Where ### 123 ### represents the id # of a company stored in database
	url(r'^(?P<company_id>[0-9]+)/$', views.companydetails, name = 'companydetails'),
	url(r'^(?P<company_id>[0-9]+)/Fundamentals/$', views.fundamentals, name = 'fundamentals'),
	url(r'^(?P<company_id>[0-9]+)/Fundamentals/Morningstar/', views.morningstar, name = 'morningstar'),#adding $ will mess up BS/IS params
	url(r'^(?P<company_id>[0-9]+)/Technicals/$', views.technicals, name = 'technicals'),
	url(r'^(?P<company_id>[0-9]+)/Technicals/Stats$', views.technicalsstats, name = 'technicalsStats'),

	#url(r'^(?P<company_id>[0-9]+)/Technicals/Image/', views.images, name = 'images'),
	
	url(r'^Images/', include('Chartjs.urls')), #root home page takes us too companies app url


]


