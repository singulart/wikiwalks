import wikipediaapi
import os 
import json
import progressbar

CATEGORY = 'Category:Feminist artists'
#CATEGORY = 'Category:Contemporary artists'

def traverse_categories_tree(categorymembers, level=0, max_level=100):
    for c in categorymembers.values():
        #print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level and interesting_category in c.title and c.title not in processed_categories:
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            processed_categories.add(c.title)
            traverse_categories_tree(c.categorymembers, level=level + 1, max_level=max_level)
        elif c.ns == wikipediaapi.Namespace.MAIN and c.title not in unique_artists:
            unique_artists.add(c.title)
            print(c.title)
            d['pages'].append({
                'name': c.title,
                'pagetext': c.text
            })

def store_categories(ctg):
    d = {'categories': list(ctg)}
    with open('categories.json', 'w') as json_file:
        json.dump(d, json_file)
    json_file.close()

def load_categories():
    if os.path.exists('categories.json'):
        with open('categories.json', 'r') as json_file:
            try:
                return json.load(json_file)['categories']
            except:
                return []
        return []

unique_artists = set()
processed_categories = load_categories()
if processed_categories:
    print('Loaded %d processed categories' % (len(list(processed_categories))))
else:
    print('No categories found, starting from scratch')
    processed_categories = set()
wiki_wiki = wikipediaapi.Wikipedia('en')
interesting_category = 'artists'
filename = 'output.json'
d = {}
with open('output.json', 'r') as existing_artists:
    d = json.load(existing_artists)
if 'pages' in d.keys():
    unique_artists = set([x['name'] for x in d['pages']])
else: 
    d['pages'] = []
    unique_artists = set()
print('Loaded %s processed artists' % (len(list(unique_artists))))

cat = wiki_wiki.page(CATEGORY)
traverse_categories_tree(cat.categorymembers)
store_categories(processed_categories)

work_result_filename = 'output.json'
with open(work_result_filename, 'w') as json_file:
    json.dump(d, json_file)



