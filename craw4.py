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

namefile = "links.txt"
def getLinkFromDisk(namefile):
    listaLink=[]
    file = open(namefile,"r")
    msj=file.readline()
    lista=list(msj.split(','))
    #return lista
    #return msj
    for i in range(len(lista)):
        listaLink.append(lista[i])
    return listaLink


quote_page=[]
#quote_page.append(getLinkFromDisk(namefile))
quote_page=getLinkFromDisk(namefile)

# for a in quote_page:
#     print a
# print "FIN"
#quote_page = []
#quote_page = getLinks(url)
#quote_page = ["https://elcomercio.pe/economia/peru/sector-construccion-seria-afectado-vacancia-presidencial-noticia-482656","https://elcomercio.pe/economia/peru/aeropuerto-chinchero-hay-acuerdo-compra-terreno-noticia-482608"]
#quote_page = ['http://elcomercio.pe/elcomercio/politica/ppk-podra-asistido-abogado-jueves-noticia-482620','http://elcomercio.pe/elcomercio/politica/pedido-vacancia-ausencia-voto-cuentan-noticia-482635']
# specify the url
#quote_page = "https://elcomercio.pe/archivo"
#quote_page = "http://www.bloomberg.com/quote/SPX:IND"
#quote_page = ["http://www.bloomberg.com/quote/SPX:IND", "http://www.bloomberg.com/quote/CCMP:IND"]
#quote_page = "https://elcomercio.pe/economia/peru/sector-construccion-seria-afectado-vacancia-presidencial-noticia-482656"
#quote_page = ["https://elcomercio.pe/economia/peru/sector-construccion-seria-afectado-vacancia-presidencial-noticia-482656","https://elcomercio.pe/economia/peru/aeropuerto-chinchero-hay-acuerdo-compra-terreno-noticia-482608"]
print "TIPO-> ",type(quote_page)
print quote_page[0]
# for a in quote_page:
#     print a
# print "FIN"

# page = urllib2.urlopen(quote_page[1])
# soup = BeautifulSoup(page, 'html.parser')
# title_box = soup.find('h1',attrs={'class':'news-title'})
# newtitles = title_box.text.encode('utf-8').strip().lower()
# #newtitles = title_box.get_text()
# print "TITULO: ",newtitles

# #sumario
# summary_box = soup.find('h2',attrs={'class':'news-summary'})
# summaries = summary_box.text.lower()
# print "SUMARIO: ",summaries
#tam = len(quote_page)

#for i in range (0,tam-1):
for pg in quote_page:
    # query the website and return the html to the variable 'page'
    page = urllib2.urlopen(pg)
    #page = urllib2.urlopen(quote_page[i])

    # parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page, 'html.parser')

    #titulo
    title_box = soup.find('h1',attrs={'class':'news-title'})
    newtitles = title_box.text.encode('utf-8').strip().lower()
    #newtitles = title_box.get_text()
    print "TITULO: ",newtitles

    #sumario
    summary_box = soup.find('h2',attrs={'class':'news-summary'})
    summaries = summary_box.text.lower()
    print "SUMARIO: ",summaries








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
