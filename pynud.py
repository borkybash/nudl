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
    

print(get_search_url(sys.argv[1:]))
search_url = get_search_url(sys.argv[1:])
