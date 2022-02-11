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
    print(titles[0])

search_url = get_search_url(sys.argv[1:])
search_html = get_search_html(search_url)
get_search_titles(search_html)

