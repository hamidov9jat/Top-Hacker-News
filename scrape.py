import operator
import pprint
import re

import requests
from bs4 import BeautifulSoup


def extract_votes(sublines: list):
    votes = []
    for subline in sublines:
        if subline.span:
            vote = subline.span.getText()
            vote = re.sub(r'\s+[a-z]*', '', vote)
            votes.append(int(vote))
        else:
            votes.append(0)

    return votes


def sort_news_by_votes(hacker_news):
    return sorted(hacker_news, key=operator.itemgetter('votes'), reverse=True)


def create_custom_hn(links, votes):
    hacker_news = []
    for link_, points in zip(links, votes):
        title = link_.getText()
        link = link_.get('href')
        # Getting news with more than 100 votes (included)
        if points > 99:
            hacker_news.append({'title': title, 'link': link, 'votes': points})

    return sort_news_by_votes(hacker_news)


def top_hn_from_several_pages(pages: list[int]):
    if min(pages) <= 0:
        raise ValueError('Page number in the list should be positive!')

    links = []
    votes = []
    for page in pages:
        res = requests.get('https://news.ycombinator.com/' + '?p=' + str(page))
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('.titleline')
        sublines = soup.select('.subline')

        links += [title.a for title in titles]
        votes += extract_votes(sublines)

    top_hacker_news = create_custom_hn(links, votes)

    return top_hacker_news


def get_top_hn(page: int):
    if page <= 0:
        raise ValueError('Page number should be positive!')

    res = requests.get('https://news.ycombinator.com/' + '?p=' + str(page))

    soup = BeautifulSoup(res.text, 'html.parser')

    titles = soup.select('.titleline')
    links = [title.a for title in titles]
    sublines = soup.select('.subline')
    votes = extract_votes(sublines)
    top_hacker_news = create_custom_hn(links, votes)

    return top_hacker_news


def main():
    # page1_top_news = get_top_hn(1)
    # page2_top_news = get_top_hn(2)
    # top_news = sort_news_by_votes(page1_top_news + page2_top_news)

    top_news = top_hn_from_several_pages([1, 2])
    pprint.pprint(top_news)


if __name__ == '__main__':
    main()
