import sys, os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import bs4
import datetime
import logging
import PyRSS2Gen
import re
import urllib2
import urlparse

log = logging.getLogger()
log.setLevel(logging.DEBUG)

url = "http://www.koka36.de/neu_im_vorverkauf.php"

def make_external(url):
    return urlparse.urljoin("http://www.koka36.de", url)


def get_feed(event, context):
    html = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    items = []

    for event in soup.find_all('div', {'class': 'event_box'}):

        data = event.find('div', {'style': 'imagefield'})

        title = data.find('p').string
        description = data.find_all('div')[-1].string
        image = make_external(data.find('img').get('src'))
        link = make_external(event.find('a').get('href'))

        if title:
            item = PyRSS2Gen.RSSItem(
                    title = title,
                    link = link,
                    description = description,
                    guid = PyRSS2Gen.Guid(link))

            items.append(item)

    rss = PyRSS2Gen.RSS2(
            title = "Neu im Vorverkauf",
            link = "http://www.koka36.de/",
            description = "Generated using bs4, PyRSS2Gen",
            lastBuildDate = datetime.datetime.utcnow(),
            items = items)

    return rss.to_xml()
