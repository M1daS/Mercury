# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Profile(models.Model):
	ticker = models.CharField(max_length = 10, default = 'TICKER')
	sector = models.CharField(max_length = 250)
	industry = models.CharField(max_length = 250)
	employees = models.CharField(max_length = 250)
	logo = models.CharField(max_length = 1000) #URl to company logo
	description = models.CharField(max_length = 6000)


	#dunder str is a string representation of this object for when you try to print or return it
	def __str__(self):
		return self.ticker + '  :  ' + self.sector




class News(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	#News is linked to a companies profile w/ foreign key
	#if the Profile is deleted, 'on_delete' then also deletes the news
	rssfeedurl = models.CharField(max_length = 5000)
	rss2html = models.CharField(max_length = 5000, default = 'null')

	def __str__(self):
		return self.rssfeedurl







import pandas as pd
import csv as csv
# Create your models here.

import sys
import os
INNER_MIDAS_DIR =  os.path.dirname(os.path.abspath('Mercury/Pathsfile.py'))
sys.path.insert(0, INNER_MIDAS_DIR)


import Pathsfile as pf
sys.path.insert(0, pf.p_MYMODULES)

import BalanceSheet as b_s
import IncomeStatement as i_s
import Buffett as buf
import Vause as vause
import Competitors as comp

MORNINGSTAR_PATH = pf.p_FINANCIAL_DATA
OUTPUT_PATH = pf.p_PRGM_OUTPUT


class Morningstar(models.Model):

	def __str__(self):
		return self.title  



	def displaydata(self, sheet_type, ticker, year):
		YEAR = year
		p = os.path.dirname(os.path.abspath('Companies/templates/morningstar.html'))
		htmlpath = p + "/morningstar.html"

		print('html', htmlpath)

		cpath = os.path.dirname(os.path.abspath('Companies/templates/morningstar.html'))
		competpath = pf.p_FINANCIAL_DATA + "/Competitors.csv"

		#Determing proper File Path based upoon Sheet Type from Button Pressed
		if sheet_type == 'BS': 
			path = MORNINGSTAR_PATH + str(YEAR) + '/' + ticker + '/' + ticker + ' Balance Sheet.csv'
			output_path = b_s.get_balance_sheet(ticker, path, MORNINGSTAR_PATH, YEAR )
			print('readpath', path)
		elif sheet_type == 'IS':
			path = MORNINGSTAR_PATH + str(YEAR) + '/' + ticker + '/' + ticker + ' Income Statement.csv'
			output_path = i_s.get_income_statement(ticker, path, MORNINGSTAR_PATH, YEAR )
		elif sheet_type == 'Buffett':
			path = MORNINGSTAR_PATH + str(YEAR) + '/' + ticker + '/' + ticker + ' Balance Sheet.csv'
			b_s.get_balance_sheet(ticker, path, MORNINGSTAR_PATH, YEAR )
			path = MORNINGSTAR_PATH + str(YEAR) + '/' + ticker + '/' + ticker + ' Income Statement.csv'
			i_s.get_income_statement(ticker, path, MORNINGSTAR_PATH, YEAR )
			path_bs = MORNINGSTAR_PATH + str(YEAR) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' Balance Sheet.csv'
			path_is = MORNINGSTAR_PATH + str(YEAR) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' Income Statement.csv'
    
			output_path = buf.get_buffett_metrics(ticker, MORNINGSTAR_PATH, path_bs, path_is, OUTPUT_PATH, YEAR)
		elif sheet_type == 'Vause':
			path = MORNINGSTAR_PATH + str(YEAR) + '/' + ticker + '/' + ticker + ' Balance Sheet.csv'
			b_s.get_balance_sheet(ticker, path, MORNINGSTAR_PATH, YEAR )
			path = MORNINGSTAR_PATH + str(YEAR) + '/' + ticker + '/' + ticker + ' Income Statement.csv'
			i_s.get_income_statement(ticker, path, MORNINGSTAR_PATH, YEAR )
			path_bs = MORNINGSTAR_PATH + str(YEAR) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' Balance Sheet.csv'
			path_is = MORNINGSTAR_PATH + str(YEAR) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' Income Statement.csv'
    
			output_path = vause.get_vause_metrics(ticker, MORNINGSTAR_PATH, path_bs, path_is, OUTPUT_PATH, YEAR)

		elif sheet_type == 'BuffettCompetitors':
			output_path = comp.get_competitor_metrics(ticker, sheet_type, competpath, MORNINGSTAR_PATH, OUTPUT_PATH, YEAR)

		elif sheet_type == 'VauseCompetitors':
			output_path = comp.get_competitor_metrics(ticker, sheet_type, competpath, MORNINGSTAR_PATH, OUTPUT_PATH, YEAR)


		datalist = []
		with open(output_path) as datafile:
			datareader = csv.reader(datafile)
			for item in datareader:
				datalist.append(item)
			df = pd.DataFrame(datalist)
			df.columns = df.iloc[0]#IMPERITIVE - THE DATA ONLY ALLIGNS PROPERLY FOR COLOR CODING WHEN IT THINKS THERE ARE TWO COLUMN NAME LINES....
			#you can fix the stupidity above by removing the duplicate header thats in the dataframe for some reason you lazy pos....
			#print(df)


		htmlfile = open(htmlpath, "w")

		htmlfile.write("{% ")
		htmlfile.write("include 'fundamentals.html' %}")
		htmlfile.write('<table border="1" align = "center" frame = "border" width = "100%"> ')

		rownum = 0
		columnum = 0
		
		with open(output_path) as file:
			reader = csv.reader(open(output_path))
			for row in reader:
				if rownum == 0:
					htmlfile.write('<tc>')
					for column in row:
						htmlfile.write('<th bgcolor = "pink">' + "<font color='black' >" + column + "</font>" + '</th>')
						htmlfile.write('</tc>')

				else:
					htmlfile.write('<tr>')
					for column in row:
						if columnum == 0: #Metric
							htmlfile.write('<td  bgcolor = "pink">' +  "<font color='black'>" + column + "</font>" + '</td>')
						elif columnum == 1: #No Color Coding available
							htmlfile.write('<td  bgcolor = "pink">' + "<font color='black'>" + column + "</font>" + '</td>')
						elif columnum > 1:
							try:
								#print(df.iloc[rownum][columnum]) #old way no longer needed - useful with different type of foor loop
								current_data = float(column)
								previous_data = float(df.iloc[rownum][columnum-1])
								if current_data > previous_data:
									htmlfile.write('<td  bgcolor = "lightgreen">' + "<font color='black'>" + column + "</font>" + '</td>')
									htmlfile.write('</tc>')
								elif current_data < previous_data:
									htmlfile.write('<td  bgcolor = "red">' + "<font color='black'>" + column + "</font>" + '</td>')
									htmlfile.write('</tc>')
							except(ValueError):
								htmlfile.write('<td  bgcolor = "pink">' + "<font color='black'>" + 'Null(ValErr)' + "</font>" + '</td>')
								htmlfile.write('</tc>')
						columnum +=1
				
				htmlfile.write('<tr>')
				rownum += 1
				columnum = 0 #Reset column number back to 0 after looping through entire row


			htmlfile.write('<table>')
			htmlfile = open(htmlpath, "r")
	
