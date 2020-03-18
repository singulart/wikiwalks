import requests
import json
import progressbar
from lxml import html
wikipage = input()
filename = 'categories.json'
response = requests.get(
       'https://en.wikipedia.org/w/api.php',
       params={
               'action': 'query',
		
               'format': 'json',
               'page': wikipage
       }).json()
raw_html = response['parse']['text']['*']

document = html.document_fromstring(raw_html)

names = document.xpath('//div[@class=\"mw-parser-output\"]/ul/li/a/@href')
d = {'artists': []}
for n in progressbar.progressbar(names):
	artist_text = requests.get('https://en.wikipedia.org/w/api.php',
       		params={
               		'action': 'query',
               		'format': 'json',
               		'titles': n.split("/")[2],
			'prop': 'extracts',
			'explaintext': 1,
			'exsectionformat': 'plain'
       		}).json()
	try:
		page = next(iter(artist_text['query']['pages'].values()))
		d['artists'].append({
			'name': page['title'], 
			'text': page['extract'], 
			'labels': []
		})
	except:
		print("Error")

with open('person.txt', 'w') as json_file:
	json.dump(d, json_file)	
