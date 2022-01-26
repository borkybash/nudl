#!/usr/bin/python3
# pynud: retrieve nudity info from movie database site

import sys

args = "+".join(sys.argv[1:])
search_query = "https://www.imdb.com/find?q=" + args
print(search_query)

