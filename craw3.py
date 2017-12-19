#obtencion de titulo,contenido,etc de 1 noticia
# import libraries
import codecs
import urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# specify the url
#quote_page = "https://elcomercio.pe/archivo"
#quote_page = "http://www.bloomberg.com/quote/SPX:IND"

#quote_page = ["http://www.bloomberg.com/quote/SPX:IND", "http://www.bloomberg.com/quote/CCMP:IND"]

quote_page = "https://elcomercio.pe/economia/peru/sector-construccion-seria-afectado-vacancia-presidencial-noticia-482656"


# query the website and return the html to the variable 'page'
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable soup
soup = BeautifulSoup(page, 'html.parser')

#titulo
title_box = soup.find('h1',attrs={'class':'news-title'})
newtitles = title_box.text.strip()
newtitles = newtitles.encode('ascii', 'ignore').decode('ascii')
print "TITULO: ",newtitles

#sumario
summary_box = soup.find('h2',attrs={'class':'news-summary'})
summaries = summary_box.text
print "SUMARIO: ",summaries

#content_box = soup.find('p',attrs={'class':'parrafo first-parrafo '})
content_box = soup.find('div',attrs={'class':'news-text-content'})
content = content_box.text
print "CONTENIDO: ",content

file = codecs.open("craw3.txt","w","utf-8")
file.write(u'\xf3')
file.write(summaries)
file.write(content)
file.close()






#open a csv file with append, so old data will not be erased 
# with open ('index.csv','a') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow([name, price, datetime.now()])

# open a csv file with append, so old data will not be erased
# with open('index.csv', 'a') as csv_file:
#     writer = csv.writer(csv_file)
#     # The for loop
#     for name, price in data:
#         writer.writerow([name, price, datetime.now()])