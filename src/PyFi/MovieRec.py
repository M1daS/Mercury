import pandas as pd 
import numpy as np
from sklearn import cross_validation as cv
from sklearn.metrics.pairwise import pairwise_distances
import re

def get_movies(p):
	r_cols = ['movie_id', 'title', 'genres']
	path = p + 'movies.csv'
	movies = pd.read_csv(path, sep = ',', names = r_cols, encoding = 'latin-1', skiprows = 1)
	movies.columns = ['movieId', 'title', 'genres']
	return movies

def get_ratings(p):
	r_cols = ['userId','movieId','rating','timestamp']
	path = p + 'ratings.csv'
	rating = pd.read_csv(path, sep = ',', names = r_cols, encoding = 'latin-1', skiprows = 1)
	ratings = rating.sort_values(by = 'movieId')
	return ratings


def get_links(p):
	r_cols = ['movieId','imdbId','tmdbId']
	path = p + 'links.csv'
	links = pd.read_csv(path, sep = ',', names = r_cols, encoding = 'latin-1', skiprows = 1)
	return links




def init(path):
	print(path)
	df = pd.DataFrame()
	movies = get_movies(path)
	ratings = get_ratings(path)
	links = get_links(path)



	n_users = ratings['userId'].unique().shape[0]
	n_items = ratings['movieId'].unique().shape[0]
	print('Number of users = ' + str(n_users) + ' | Number of movies = ' + str(n_items))


	df = pd.merge(movies, ratings, on="movieId")
	full_df = pd.merge(df, links, on="movieId")


	dates_list = []
	for s in full_df.title:
		date = s[s.find("(")+1:s.find(")")]
		try:
			date = int(date)
		except:
			date = 0
		dates_list.append(date)
	full_df['Date'] = dates_list



	#ML RECOMENDATION AGE
	currentuser = 672
	ratings_pivot_table  = full_df.pivot_table('rating', index = 'movieId', columns = 'userId')
	user_ratings = ratings_pivot_table[currentuser]
	user_correlation = ratings_pivot_table.corrwith(user_ratings)

	full_df_reduced = full_df[user_ratings[full_df.movieId].isnull().values & (full_df.userId != currentuser) & (full_df.Date > 1900)]
	full_df_reduced['similarity'] = full_df_reduced['userId'].map(user_correlation.get)
	full_df_reduced['sim_rating'] = full_df_reduced['similarity'] * full_df_reduced.Date
	print(full_df_reduced.head())


	recomend = full_df_reduced.groupby('movieId').apply(lambda s: s['sim_rating'].sum() / s['similarity'].sum())
	print(recomend.head())

	sortedrec = recomend.sort_values(ascending = False)
	
	recitems = sortedrec.index[:50]
	recomended_titles = []
	for anID in recitems:
		output = full_df[full_df['movieId'] == anID]
		title = output['title'].to_string() 
		cleaned_title = re.sub(r'\([^)]*\)', '', title) #remove all parenthesis
		cleaned_title2 = cleaned_title.split('\n')[0] #remove all movie ids  after \n
		cleaned_title3 = cleaned_title2.split(' ', 1)[-1] #remove all digits in front the first space and split only first occurance

		recomended_titles.append(cleaned_title3)

	df = pd.DataFrame()
	df['Movies'] = recomended_titles


	part1 = recomended_titles[:16]
	part2 = recomended_titles[17:33]
	part3 = recomended_titles[34:]

	return (part1, part2, part3)






def get_user_ratings(path):
	df = get_ratings(path)
	userdata = df[df.userId == 672]
	user_movieids = userdata.movieId


	allmovies = get_movies(path)
	allmovies = allmovies.set_index(['movieId'])

	user_rated_movies = []
	for item in user_movieids:
		user_rated_movies.append(allmovies['title'].ix[item])

	return user_rated_movies