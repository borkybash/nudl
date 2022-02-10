#!/usr/bin/python3
# pynud: retrieve nudity info from movie database site

import sys
import requests, bs4

def get_search_url(args):
    args = "+".join(args)
    search_url = "https://www.imdb.com/find?q=" + args
    return search_url

print(get_search_url(sys.argv[1:]))

