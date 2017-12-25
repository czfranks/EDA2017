try: import simplejson as json
except ImportError: import json
#from PIL import Image
from urllib import urlopen
from StringIO import StringIO
import urlparse
import urllib
import os
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#script olny for CORREO
diariocorreo = "https://diariocorreo.pe"

def normalize(s):
	s=s.lower()
	ans=""
	i=0
	n = len(s)
	while(i<n and not s[i].isalpha()):  
		i+=1
	while(i<n and s[i].isalpha() ):
		ans+=s[i]
		i+=1
	return ans 

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
	soup = BeautifulSoup(newHtml,"html.parser")

	file = open("page.txt", "a")

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
					crawler_url_news(urlnoticia,file)



	

def crawler_url_news(urlnews,file): #crawlear solo una noticia de un html con url="urlnews"
	try:
		newHtml = urllib.urlopen(urlnews).read()
	except:
		print "error"
	soup = BeautifulSoup(newHtml,"html.parser")

    #titulo de la noticia ---------------------------- string
	titleObj = soup.find(itemprop="headline")
	arrTitleNorm = []
	if(titleObj):
		title = titleObj.get_text()
		print title
		arrTitle = title.split(" ") 
		for w in arrTitle:
			palabra = normalize(w.strip())
			if(len(palabra)>=3):
				arrTitleNorm.append(palabra)
		file.write(str(len(arrTitleNorm)))
		file.write("\n")
		for w in arrTitleNorm:
			file.write(w)
			file.write(" ")
		file.write("\n")

	#fecha de publicacion ---------------------------- string
	dateObj = soup.find(attrs={"class":"date-publish"})
	if(dateObj):
		dateContent = dateObj['content']
		if(dateContent):
			date = dateContent
			file.write(normalize(date.strip()))
			file.write("\n")

	#texto de la noticia ----------------------------- string
	bodytext = ""
	artBody = soup.find(itemprop="articleBody")
	arrBodyNorm = []
	if(artBody):
		for tag_p in artBody.find_all('p'):
		    if(tag_p):
				if(not tag_p.find_all('script')):
			    	#print TextNews1
					sentence = tag_p.get_text()#.decode('unicode-escape')
					#bodytext=bodytext + sentence
					arrBody = sentence.split(" ")
					
					for w in arrBody:
						palabra = normalize(w)
						if(len(palabra)>=3):
							arrBodyNorm.append(palabra)
					
	if(len(arrBodyNorm)<=1):
		file.write(str(len(arrTitleNorm)))
		file.write("\n")
		for w in arrTitleNorm:
			file.write(w)
			file.write(" ")
	else:
		file.write(str(len(arrBodyNorm)))
		file.write("\n")
		for w in arrBodyNorm:
			file.write(w)
			file.write(" ")
	file.write("\n")
	#print bodytext	
	print "---------------------------------------------------------"



##ejemplos de ejecucion en las funciones
#crawler_url_news("https://diariocorreo.pe/politica/abogados-presentan-demanda-de-amparo-ante-el-pj-contra-vacancia-de-ppk-792648/")
for i in range(4,11):
	crawler_page_i_esima ("https://diariocorreo.pe/politica/?page="+str(i),"politica")


## GENERAR AHORA https://diariocorreo.pe/tema/?page=3 -> TEMA DEBE SER LLAMADO PARA POLITICA, ESPECTACULOS, DEPORTES, ETC

