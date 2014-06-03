# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries. You can use whatever libraries are installed
# on Morph for Python (https://github.com/openaustralia/morph-docker-python/blob/master/pip_requirements.txt) and all that matters
# is that your final data is written to an Sqlite database called data.sqlite in the current working directory which
# has at least a table called data.

###############################################################################
# CASC scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time

# retrieve a page
starting_url = 'http://www.hmrc.gov.uk/casc/clubs.htm'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
paras = soup.findAll(id='centre_col')
for a in paras:
    anchors = a.findAll('a')
    for b in anchors:
        try:
            length = len(b.text)
        except ValueError:
            length = 0
        if length==1:
            page_url = 'http://www.hmrc.gov.uk/casc/' + b['href']
            page_html = scraperwiki.scrape(page_url)
            #print url
            page_soup = BeautifulSoup(page_html)
            trs = page_soup.findAll('tr') 
            for tr in trs:
                tds = tr.findAll('td')
                if len(tds)==0:
                    continue
                else:
                    try:
                        name = tds[0].contents[0]
                    except IndexError:
                        name = ""
                    try:
                        address = tds[1].contents[0]
                    except IndexError:
                        address = ""
                    try:
                        postcode = tds[2].contents[0]
                    except IndexError:
                        postcode = ""
                    record = { "name" : name , "address" : address , "postcode" : postcode }
                    print record
                    scraperwiki.sqlite.save(["name"], record) 
