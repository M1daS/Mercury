from django.db import models

import pandas as pd
import csv as csv

# Create your models here.
class CryptoData(models.Model):

	def displaydata(self, output_path, output_path2, htmlpath):
		htmlfile = open(htmlpath, "w")
		htmlfile.write("{% ")
		htmlfile.write("include 'Base1.html' %}")
		htmlfile.write('<table border="1" align = "center" frame = "border" width = "100%"> ')

		rownum = 0
		columnum = 0
		
		with open(output_path) as file:
			reader = csv.reader(open(output_path))
			for row in reader:
				htmlfile.write('<tc>')
				for column in row:
					htmlfile.write('<th bgcolor = "#ffffff">' + "<font color='black' >" + column + "</font>" + '</th>')
					htmlfile.write('</tc>')
					columnum +=1
				
				htmlfile.write('<tr>')
				rownum += 1
				columnum = 0 #Reset column number back to 0 after looping through entire row


			htmlfile.write('<table>')
			htmlfile = open(htmlpath, "r")