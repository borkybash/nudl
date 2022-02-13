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

def get_nudity_list(id):
    parents_guide_url = f'https://www.imdb.com{id}parentalguide'
    res = requests.get(parents_guide_url)
    res.raise_for_status()
    parents_guide_html = bs4.BeautifulSoup(res.text, features='html.parser')
    nudity_elems = parents_guide_html.select('#advisory-nudity li.ipl-zebra-list__item')
    nudity_list = []
    for i in range(len(nudity_elems)):
        nudity_list.append(nudity_elems[i].getText().strip().rstrip('Edit').strip())
    return nudity_list

def display_nudity_info(title, items):
    print(title)
    for i in items:
        print('\n' + i)

search_url = get_search_url(sys.argv[1:])
search_html = get_search_html(search_url)
search_titles = get_search_titles(search_html)
search_ids = get_search_ids(search_html)
nudity_list = get_nudity_list(search_ids[0])
display_nudity_info(search_titles[0], nudity_list)
