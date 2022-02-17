#!/usr/bin/env python3
# pynud: retrieve nudity info from movie database site

import sys
import requests, bs4, click

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
    for _, title in enumerate(title_elems):
        titles.append(title.getText().strip())
    return titles


def get_search_ids(html):
    id_elems = html.select('.result_text a')
    ids = []
    for _, id_elem in enumerate(id_elems):
        title_id = id_elem.attrs['href']    
        ids.append(title_id)
    return ids 


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


def show_nudity_info(nudity_list, title):
    click.echo("\n" + title + "\n")
    for _, item in enumerate(nudity_list):
        click.echo(item)
        click.echo()
    

@click.command()
@click.argument('movie_title', nargs=-1, required=True)
def main(movie_title):
    """Display nudity information for given movie title."""

    search_url = get_search_url(movie_title)
    search_html = get_search_html(search_url)
    search_titles = get_search_titles(search_html)
    search_ids = get_search_ids(search_html)
    nudity_list = get_nudity_list(search_ids[0])
    show_nudity_info(nudity_list, search_titles[0])


if __name__ == '__main__':
    main()
