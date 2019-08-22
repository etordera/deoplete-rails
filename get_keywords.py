#!/usr/local/bin/python3
import urllib.request
import json
import re

api_index_url = 'https://api.rubyonrails.org/js/search_index.js'

# Download index js and parse data as JSON
fp = urllib.request.urlopen(api_index_url)
api_index = fp.read().decode('utf8')
fp.close()
api_index = api_index[api_index.find('{'):]
api_json = json.loads(api_index)

# Generate unique and sorted method names list
methods = []
for name in api_json['index']['searchIndex']:
    matches = re.search('^([A-Za-z_]+[!?]?)\(\)$', name)
    if matches:
        methods.append(matches.group(1))
methods = list(set(methods))
methods.sort()

# Generate unique and sorted class names list
classes = []
for data in api_json['index']['info']:
    for name in data[0].split('::'):
        if re.match('^[A-Z][A-Za-z]+$', name):
            classes.append(name)
classes = list(set(classes))
classes.sort()

# Generate formatted output
keywords = methods + classes
print('rails_keywords = [', end='')
line_length = 0
for i in range(len(keywords)):
    if line_length == 0:
        print("\n    ", end='')
        line_length = 4
    print("'" + keywords[i] + "'", end='')
    if i < len(keywords)-1:
        print(',', end='')
        line_length += len(keywords[i]) + 1
        if line_length < 80:
            print(' ', end='')
        else:
            line_length = 0
print("\n]")
