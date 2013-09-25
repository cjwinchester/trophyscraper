"""
Scrapin' the Nebraska Game and Parks Big Game Trophy database.
"""

from mechanize import Browser
from bs4 import *
from time import *
import re

# Crank up a browser
mech = Browser()

# Add a user-agent string
mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = "http://outdoornebraska.ne.gov/trophy/"

# Open the file what needs writing to
f = open('trophies.txt', 'wb')

# Beautiful soup that bizzo
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

# Target the number of the last page to step through with a regular expression, store as an integer
regexin = re.search(r'Page \d\r\n\s+of \d+', str(soup))

targetpage = re.sub(r"\s+","", regexin.group().replace("\r\n",""))

pagelimit = int(targetpage[targetpage.find("f")+1:])

print 'Pages to scrape: ' + str(pagelimit) + '\n====================\n'

paging = 1

# Loop through the table on each page 
while (paging <= pagelimit):
   print 'Scraping page', paging
   table = soup.find("table", class_="data-grid")
   for row in table.findAll('tr')[2:]:
       col = row.findAll('td')
       year = col[0].string
       score = col[1].string
       species = col[2].string
       weapon = col[3].string
       type = col[4].string
       county = col[5].string
       first = col[6].string
       last = col[7].string
       city = col[8].string
       details = 'http://outdoornebraska.ne.gov' + col[9].find('a').get('href')
       animals = (year.strip(), score.strip(), species.strip(), weapon.strip(), type.strip(), county.strip(), first.strip(), last.strip(), city.strip(), details.strip(),"\n")
       f.write("\t".join(animals))
   sleep(5)
   nextpage = mech.follow_link(text_regex="Next >")
   nexthtml = nextpage.read()
   soup = BeautifulSoup(nexthtml)
   paging = paging + 1
   if paging = pagelimit:
       pass
   
f.close()
