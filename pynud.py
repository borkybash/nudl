#!/usr/bin/python3
# pynud: retrieve nudity info from movie database site

import sys
import requests, bs4

def get_search_url(args):
    args = "+".join(args)
    search_url = "https://www.imdb.com/find?q=" + args
    return search_url

def get_search_html(url):
    res = requests.get(url)
    res.raise_for_status()
    search_html = bs4.BeautifulSoup(res.text, features='html.parser')
    return search_html
    
def get_search_titles(html):
    title_elems = html.select('.result_text')
    titles = []
    for i in range(len(title_elems)):
        titles.append(title_elems[i].getText().strip())
    return titles

def get_search_ids(html):
    id_elems = html.select('.result_text a')
    ids = []
    for i in range(len(id_elems)):
        title_id = id_elems[0].attrs['href']    
        ids.append(title_id)
    return ids 

search_url = get_search_url(sys.argv[1:])
search_html = get_search_html(search_url)
print(get_search_titles(search_html)[0])
print(get_search_ids(search_html)[0])

