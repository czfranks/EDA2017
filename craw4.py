'''
1.- extraer links en un array
2.- extraer de cada link o noticia: titulo, contenido
'''

#obtencion de VARIAS noticias
# import libraries
import urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

url ="https://elcomercio.pe/peru"

#obtener links
def getLinks(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page,'html.parser')
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("https://elcomercio.pe/")}):
        links.append(link.get('href').encode("utf-8").strip()) 
    return links
#print( getLinks("https://elcomercio.pe/"))
#print( getLinks("https://elcomercio.pe/peru") )

quote_page = []
quote_page = getLinks(url)

# specify the url
#quote_page = "https://elcomercio.pe/archivo"
#quote_page = "http://www.bloomberg.com/quote/SPX:IND"
#quote_page = ["http://www.bloomberg.com/quote/SPX:IND", "http://www.bloomberg.com/quote/CCMP:IND"]
#quote_page = "https://elcomercio.pe/economia/peru/sector-construccion-seria-afectado-vacancia-presidencial-noticia-482656"
#quote_page = ["https://elcomercio.pe/economia/peru/sector-construccion-seria-afectado-vacancia-presidencial-noticia-482656","https://elcomercio.pe/economia/peru/aeropuerto-chinchero-hay-acuerdo-compra-terreno-noticia-482608"]

for pg in quote_page:
    # query the website and return the html to the variable 'page'
    page = urllib2.urlopen(pg)

    # parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page, 'html.parser')

    #titulo
    title_box = soup.find('h1',attrs={'class':'news-title'})
    newtitles = title_box.text.encode('utf-8').strip()
    #newtitles = title_box.get_text()
    print "TITULO: ",newtitles

    #sumario
    summary_box = soup.find('h2',attrs={'class':'news-summary'})
    summaries = summary_box.text
    print "SUMARIO: ",summaries

#name = name_box.text.strip() # strip() is used to remove starting and trailing
#print name






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