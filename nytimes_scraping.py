# nytimes scraping

from nytimesarticle import articleAPI
import json
import pandas as pd
import datetime

key = input('Enter your api key: ')
api = articleAPI('47948d7109eda66d76ccb67753997d53:15:28718339')


page_start = 1
page_end = 50
pages = range(page_start, page_end)
query_set = 'David Brooks'
mainDF = pd.DataFrame(columns=['headline','kicker','pub_date','page'])

for page in pages:
	articles = api.search( q = query_set, 
	     fq = {'kicker':query_set}, 
	     fl =['headline','byline','pub_date'],
	     page=page)

	article_info = []
	for article in articles['response']['docs']:
		(article_info.append({'kicker':article['headline']['kicker'],
							  'headline': article['headline']['main'],
							  'pub_date':article['pub_date'],
							  'page':page
			}))

	articleDF = pd.DataFrame(article_info)
	try:
		articleDF.to_csv('nytimes_query_results/%s_%d_%s.csv' %(query_set, page, datetime.date.today()))
		mainDF =mainDF.append(articleDF)
	except UnicodeEncodeError:
		print page, len(articleDF)

mainDF.to_csv('david_brooks_scrape_page%d_to_page%d.csv' % (page_start, page_end))
# articles = api.search( q = 'Obama', 
#      fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, 
#      begin_date = 20111231 )

# Article Search API
# Key: "47948d7109eda66d76ccb67753997d53:15:28718339"

# Most Popular API
# Key: 3075b5f1806a2b8846aa44decd126a5a:18:28718339

# Top Stories API
# Key: 3e1a47450a0256a3ba6160f14c161ecd:2:28718339