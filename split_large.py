import shelve
import simplejson

f = open('output.json', 'r')
d = simplejson.load(f)
sh = shelve.open('7k')
sh['pages'] = d['pages']
f.close()

num_items_per_file = 200
filename = '7k_[%i-%i].json'
pages = list(sh['pages'])
fileno = 1
for chunk in [ pages[x:x+num_items_per_file:] for x in range(0, len(sh['pages']), num_items_per_file)]:
    f = open(filename % (fileno, fileno+num_items_per_file - 1), 'w')
    d = {'pages': []}
    d['pages'] = chunk
    simplejson.dump(d, f, indent=4)
    f.close()
    fileno += num_items_per_file
sh.close()
