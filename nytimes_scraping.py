# nytimes scraping

from nytimesarticle import articleAPI

api = input('Enter your api key: ')
articles = api.search( q = 'Obama', 
     fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, 
     begin_date = 20111231 )
	