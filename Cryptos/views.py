

# Create your views here.

from __future__ import unicode_literals
from django.shortcuts import render
import django

from django.db import models

from django.shortcuts import render

from .models import CryptoData



import sys
import os
INNER_MIDAS_DIR =  os.path.dirname(os.path.abspath('Midas104/Pathsfile.py'))
sys.path.insert(0, INNER_MIDAS_DIR)


import Pathsfile as pf
sys.path.insert(0, pf.p_CryptoMODULES)


# import Correlate as cor
import bollingerstrat as bbs


def cryptoroot(request):
	def search():
		if 'params' in request.GET:
			x = request.GET['params']
		else:
			x = 'Form is empty'
		return x


	search()

	context = {

	}
	return render(request, 'cryptoroot.html', 	context)



def correlate(request):


	# path = pf.p_CRYPTO_DATA
	# outputpath = pf.p_PRGM_OUTPUT + 'Crypto_Correlate.csv'
	# p = os.path.dirname(os.path.abspath('Cryptos/templates/cryptodatatables.html'))
	# htmlpath = p + "/cryptodatatables.html"


	# data = cor.init(path, outputpath)

	# context = {


	# }

	# cd = CryptoData()
	# outputpath2 = 'null'
	# cd.displaydata(outputpath, outputpath2, htmlpath)



	# return render(request, 'cryptodatatables.html', context)
	return x

def bbstrat(request):

	path = pf.p_CRYPTO_DATA
	outputpathbuy = pf.p_PRGM_OUTPUT + 'Crypto_BB_Buy.csv'
	outputpathsell = pf.p_PRGM_OUTPUT + 'Crypto_BB_Sell.csv'
	p = os.path.dirname(os.path.abspath('Cryptos/templates/cryptodatatables.html'))
	htmlpath = p + "/cryptodatatables.html"

	bbs.init(path, outputpathbuy, outputpathsell)

	cd = CryptoData()
	cd.displaydata(outputpathbuy, outputpathsell, htmlpath)

	context = {


	}

	return render(request, 'cryptodatatables.html', context)

