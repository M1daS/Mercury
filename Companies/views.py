
from __future__ import unicode_literals
from django.shortcuts import render
import django

from django.db import models

from .models import Profile, News

from django.shortcuts import render

from django.http import Http404

from .models import Morningstar


import pandas as pd
import sys
import os
INNER_MIDAS_DIR =  os.path.dirname(os.path.abspath('Midas104/Pathsfile.py'))
sys.path.insert(0, INNER_MIDAS_DIR)


import Pathsfile as pf
sys.path.insert(0, pf.p_MYMODULES)


import csv
import var as var
import ttest as tt
import OptimalPortfolio as op
import MonteCarlo as mc
import HistoricalQuoteRetrieve as hqr
import Bloomberg as bloom
import NewsRSS as news

from django.views import generic


def companies(request):

	all_companies = Profile.objects.all()

	indexnames = ['comp', 'djia', 'spx', 'rut', 'vix']
	indexnames_converted = ['NASDAQ', "DJIA", 'SAP500', "IWM", 'VIX']
	df = bloom.bloomberg_index(indexnames)
	print(df)


	close = df['close']
	pointchange = df['pointchange']
	pctchange = df['pct']


	data = news.start_rss(pf.p_PRGM_OUTPUT + 'NewsRss.csv')



	context = {
		'Profile_objects':all_companies,
		'indexnames':indexnames_converted,
		'close':close,
		'pointchange':pointchange,
		'pctchange':pctchange,
		"news":data,

	}


	return render(request, 'companies.html', context)





def watchlist(request):
	current_user = request.user
	cookiepath = pf.p_Cookies + '/' + 'Cookies_' + str(current_user) +'.csv'

	import os.path
	if os.path.isfile(cookiepath) == False:
		file = open(cookiepath, 'w') 


	def search():
		if 'watchlist_tickers' in request.GET:
			companies = request.GET['watchlist_tickers']
			watchlist = companies.split(' ')
		else:
			with open(cookiepath, 'r') as f:
				watchlist = f.readline().split(',')
		return watchlist
	watchlist = search()

	request.session['watchlist'] = watchlist
	watchlist = request.session.get('watchlist', 'blahblah') 
	print(watchlist)
	wl_list = []
	with open(cookiepath, 'w') as f:
		for item in watchlist:
			f.write(item + ',')
			wl_list.append(item)

	# indexnames = [watchlist]
	# df = bloom.marketwatch_stock(wl_list)
	# # print(df)
	


	context = {
		'wl':watchlist

	}

	return render(request, 'watchlist.html', context)












def companydetails(request, company_id):

	print(pf.p_HISTORICAL_DATA)


	profileinfo = str(Profile.objects.get(id = company_id))
	profilesplit = profileinfo.split(':')
	ticker = profilesplit[0].strip()

	try:
		timespan = '1Y'
		hqr.retrieve_historical_data(timespan, [ticker], pf.p_HISTORICAL_DATA) #ticker must be in list format
	except(Exception):
		print('Unable to download data')

	try:
		profile = Profile.objects.get(id = company_id)
		news = News.objects.get(id = company_id)

		context = {
			'profile': profile,
			'news':news

		}
	except Profile.DoesNotExist:
		raise Http404("Company Does not Exist")
	#return HttpResponse("<h2>Details for Company ID# " + str(company_id) + " </h2>")
	return render(request, 'companydetails.html', 	context)



def fundamentals(request, company_id):
	profile = Profile.objects.get(id = company_id)
	#print(profile.ticker)

	context = {
		'profile': profile,

	}
	return render(request, 'fundamentals.html', context)




def technicals(request, company_id):
	profile = Profile.objects.get(id = company_id)
	#print(profile.ticker)

	context = {
		'profile': profile,

	}

	return render(request, 'technicals.html', context)



def technicalsstats(request, company_id):
	def search():
		if 'params' in request.GET:
			x = request.GET['params']
		else:
			x = 'Form is empty'
		return x
	params = search()
	params = params.split('_')
	#co_id = params[0] #profile id number
	sheet_type = params[1] #sheet type
	print(sheet_type)

	profile = Profile.objects.get(id = company_id) #reuturns NVDA : Technology
	global ticker
	ticker = str(profile).split(':')[0]
	ticker = "".join(ticker.split())


	path = pf.p_HISTORICAL_DATA + ticker + '1Y.csv'

	p = os.path.dirname(os.path.abspath('Companies/templates/technicalsstats.html'))

	htmlpath = p + "/technicalsstats.html"
	htmlfile = open(htmlpath, "w")

	outputstring = ''
	outputstring_indexes = ''
	if sheet_type == 'VaR':
		var_out = str(var.init_var(ticker, path))
		outputstring = var_out
	if sheet_type == 'TT':
		tt_out = str(tt.init_ttest(ticker, path))
		outputstring = tt_out
	if sheet_type == 'MC':
		mc_out = mc.run_montecarlo(ticker, path)
		outputstring_indexes = ''.join(['	Mean	', '	5th Percentile	', '	95th Percentile	', '	Volatility	', '	CAGR	'])
		outputstring = ''.join(str(mc_out))
	if sheet_type == 'OP':
		alist = ['AAPL','NVDA','INTC','BABA']
		out = op.optimize(alist, YAHOO_HISTORIC_PATH)

		out.to_csv(p_PRGM_OUTPUT)



		htmlfile.write('<table>')
		rownum = 0
		columnum = 0
		with open(outpath) as file:
			reader = csv.reader(open(outpath))
			for row in reader:
				htmlfile.write('<tc>')
				for column in row:
					htmlfile.write('<th>' +  column + '</th>')
					htmlfile.write('</tc>')
				htmlfile.write('<tr>')
			htmlfile.write('<table>')


	htmlfile.write('<h3>' +  outputstring_indexes + '</h3>')
	htmlfile.write("\n")
	htmlfile.write('<h3>' +  outputstring + '</h3>')
	htmlfile = open(htmlpath, "r")

	return render(request, 'technicalsstats.html')



def morningstar(request, company_id):
	profile = Profile.objects.get(id = company_id)
	ticker = profile.ticker


	print(ticker)

	
	context = {
		'profile': profile,
	}
	mstar = Morningstar()


	def search():
		if 'sheet_type' in request.GET:
			param = request.GET['sheet_type']
		else:
			param = 'Form is empty'
		
		return param


	params = search()
	print(params)
	params = params.split('-')
	sheet_type = str(params[0])
	year = int(params[1])



	mstar.displaydata(sheet_type, ticker, year)
	return render(request, 'morningstar.html', context)




def images():
	print('images')



