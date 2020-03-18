# Iteratively extracts Wiki page content for all bullet list items from the root page (provided as input) 
import requests
import json
import progressbar
from lxml import html
wikipage = input()
filename = 'output.json'
response = requests.get(
       'https://en.wikipedia.org/w/api.php',
       params={
               'action': 'parse',
               'format': 'json',
               'page': wikipage
       }).json()
raw_html = response['parse']['text']['*']

document = html.document_fromstring(raw_html)

names = document.xpath('//div[@class=\"mw-parser-output\"]/ul/li/a/@href')
d = {'pages': []}
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
		d['pages'].append({
			'name': page['title'], 
			'pagetext': page['extract']
		})
	except:
		print("Error")

with open(filename, 'w') as json_file:
	json.dump(d, json_file)	
