
def init(dataPath, htmlPath):
	datalist = []
	with open(output_path) as datafile:
	datareader = csv.reader(datafile)
	for item in datareader:
		datalist.append(item)
	df = pd.DataFrame(datalist)
	df.columns = df.iloc[0]#IMPERITIVE - THE DATA ONLY ALLIGNS PROPERLY FOR COLOR CODING WHEN IT THINKS THERE ARE TWO COLUMN NAME LINES....
	#you can fix the stupidity above by removing the duplicate header thats in the dataframe for some reason you lazy pos....
	#print(df)


	htmlfile = open(htmlPath, "w")

	htmlfile.write("{% ")
	htmlfile.write("include 'fundamentals.html' %}")
	htmlfile.write('<table border="1" align = "center" frame = "border" width = "100%"> ')

	rownum = 0
	columnum = 0

	with open(dataPath) as file:
	reader = csv.reader(open(dataPath))
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
	htmlfile = open(htmlPath, "r")


	