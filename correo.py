try: import simplejson as json
except ImportError: import json
#from PIL import Image
from urllib import urlopen
from StringIO import StringIO
import urlparse
import urllib
import os
from bs4 import BeautifulSoup

#script olny for CORREO
diariocorreo = "https://diariocorreo.pe"

def getLinksForPagination(tema,pag_n):  #example (politica,200 paginas) 
	prefix = diariocorreo+"/"+tema+"/?page="
	suffix = "&ref=menu_top"
	pagination = ["https://diariocorreo.pe/"+tema+"/?ref=menu_top"]
	for i in range(2,pag_n+1):
		pagination.append(prefix+str(i)+suffix)
	return pagination


def crawler_page_i_esima(urlpage_i,tema): #sacar todas las urls de noticias de una pagina
	try:
		newHtml = urllib.urlopen(urlpage_i).read()
	except:
		print "error"
	soup = BeautifulSoup(newHtml)

	#print soup
	diariocorreoTema = diariocorreo+"/"+tema
	len_p = len(diariocorreoTema)

	variadas = soup.find(attrs={"class":"variadas-left"})
	if(variadas):
		#titulos de noticias
		newsTitles = variadas.find_all(attrs={"class":"title-gral"})
		if(newsTitles):
			for i in newsTitles:
				urlnoticia = diariocorreo + i.find('a',href=True)['href']
				if(urlnoticia[0:len_p] == diariocorreoTema):	
					print urlnoticia
					crawler_url_news(urlnoticia)



	

def crawler_url_news(urlnews): #crawlear solo una noticia de un html con url="urlnews"
	try:
		newHtml = urllib.urlopen(urlnews).read()
	except:
		print "error"
	soup = BeautifulSoup(newHtml)

    #titulo de la noticia ---------------------------- string
	title = soup.find(itemprop="headline").get_text().encode('utf-8')
	print title
	
	#resumen de la noticia --------------------------- string
	summary = soup.find(itemprop="description").get_text().encode('utf-8')
	#print summary

	#keywords de la noticia -------------------------- array
	keywords = soup.find(attrs={"name":"keywords"})['content'].encode('utf-8').split(',\n')
	#print keywords

	#fecha de publicacion ---------------------------- string
	date = soup.find(attrs={"class":"date-publish"})['content'].encode('utf-8')
	#print date

	#texto de la noticia ----------------------------- string
	bodytext = ""
	artBody = soup.find(itemprop="articleBody")
	if(artBody):
		for tag_p in artBody.find_all('p'):
		    if(tag_p):
			if(not tag_p.find_all('script')):
			    sentence =  tag_p.get_text().encode('utf-8')#.decode('unicode-escape')
			    #print TextNews1
			    bodytext=bodytext+sentence
	#print bodytext	
	print "---------------------------------------------------------"



#ejemplos de ejecucion en las funciones
#crawler_url_news("https://diariocorreo.pe/politica/abogados-presentan-demanda-de-amparo-ante-el-pj-contra-vacancia-de-ppk-792648/")
crawler_page_i_esima ("https://diariocorreo.pe/deportes/?page=3","deportes")

## GENERAR AHORA https://diariocorreo.pe/tema/?page=3 -> TEMA DEBE SER LLAMADO PARA POLITICA, ESPECTACULOS, DEPORTES, ETC
