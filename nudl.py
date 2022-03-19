#!/usr/bin/env python3
# pynud: retrieve nudity info from movie database site

import sys
import requests, bs4, click

# Generate search url from given arguments
def get_search_url(args):
    args = "+".join(args)
    search_url = f"https://www.imdb.com/find?q={args}&s=tt&ttype=ft"
    return search_url


# Store search page html
def get_search_html(url):
    res = requests.get(url)
    res.raise_for_status()
    search_html = bs4.BeautifulSoup(res.text, features='html.parser')
    return search_html

    
# Webscrape search page & return list of title names
def get_search_titles(html):
    title_elems = html.select("#main td.result_text")
    titles = []
    for title in (title_elems):
        titles.append(title.getText().strip())
    return titles


# Webscrape search page & return list of title IDs
def get_search_ids(html):
    id_elems = html.select("#main td.result_text a")
    ids = []
    for id_elem in (id_elems):
        title_id = id_elem.attrs['href']    
        ids.append(title_id)
    return ids 


# Webscrape parental guidance page & store nudity list
def get_nudity_list(title_id):
    parents_guide_url = f'https://www.imdb.com{title_id}parentalguide'
    res = requests.get(parents_guide_url)
    res.raise_for_status()
    parents_guide_html = bs4.BeautifulSoup(res.text, features='html.parser')
    nudity_elems = parents_guide_html.select('#advisory-nudity li.ipl-zebra-list__item')
    nudity_list = []
    for _, list_item in enumerate(nudity_elems):
        nudity_list.append(list_item.getText().strip().rstrip('Edit').strip())
    return nudity_list


# Print out movie title and nudity info to stdout
def show_nudity_info(nudity_list, title):
    click.echo("\n" + title + "\n")
    for _, item in enumerate(nudity_list):
        click.echo(item)
        click.echo()


# List search titles & prompt for title selection 
def show_title_list(search_titles):
    while True:
        selections = ["q"]
        print()
        for i, title in enumerate(search_titles[:10]):
            print(f"{i+1}) {title}")
            selections.append(str(i+1))
        print()
        title_selection = input("Enter [title #] or [q] to quit: ")
        if title_selection in selections:
            break  

    # Validate selection choice
    if title_selection.lower() == "q":
        exit()
    else:
        return (int(title_selection)-1)
    

@click.command()
@click.argument('movie_title', nargs=-1, required=True)
@click.option('-l', is_flag=True, help='Select from title list.')
def main(movie_title, l):
    """Display nudity information for given movie title."""

    search_url = get_search_url(movie_title)
    search_html = get_search_html(search_url)
    search_titles = get_search_titles(search_html)
    search_ids = get_search_ids(search_html)

    if l:
        title_index = show_title_list(search_titles)
    else:
        title_index = 0

    nudity_list = get_nudity_list(search_ids[title_index])
    show_nudity_info(nudity_list, search_titles[title_index])


if __name__ == '__main__':
    main()
