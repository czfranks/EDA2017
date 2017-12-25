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
					crawler_url_news(urlnoticia,file,first=True)
					crawler_url_news(urlnoticia,file,first=False)
					



	

def crawler_url_news(urlnews,file,first): #crawlear solo una noticia de un html con url="urlnews"
	try:
		sinOpen = urllib.urlopen(urlnews)
		newHtml = sinOpen.read()
	except:
		print "error"
	soup = BeautifulSoup(newHtml)#,"html.parser")
	if(not first):
		ok = True
		if(soup.body):
			print "BIEN!!!"
			ok = True
		else:
			ok = False
			print "MAL!!"
		
		if(ok):
			#titulo de la noticia ---------------------------- string
			titleObj = soup.find(itemprop="headline")
			arrTitleNorm = []
			arrTitleRaw = []
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
				for w in arrTitle:
					if(len(w.strip())>=1):
						arrTitleRaw.append(w)
				file.write(str(len(arrTitleRaw)))
				file.write("\n")
				for w in arrTitleRaw:
					file.write(w)
					file.write(" ")
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

			#fecha de publicacion ---------------------------- string
			#dateObj = soup.find(attrs={"class":"date-publish"})
			dateObj = soup.find(attrs={"property":"article:published_time"})
			if(dateObj):
				print dateObj['content']
				dateContent = dateObj['content']
				file.write(dateObj['content'].strip())
				file.write("\n")

			print "---------------------------------------------------------"




##ejemplos de ejecucion en las funciones
#crawler_url_news("https://diariocorreo.pe/politica/alan-garcia-manda-carta-de-agradecimiento-comision-lava-jato-792962/",file=open("algo","a"))
#crawler_page_i_esima ("https://diariocorreo.pe/politica/?page=3","politica)
for i in range(3,123):
	crawler_page_i_esima ("https://diariocorreo.pe/politica/?page="+str(i),"politica")

## GENERAR AHORA https://diariocorreo.pe/tema/?page=3 -> TEMA DEBE SER LLAMADO PARA POLITICA, ESPECTACULOS, DEPORTES, ETC

#crawler_url_news("https://diariocorreo.pe/politica/ollanta-humala-no-vacancia-ppk-peligro-no-ha-pasado-793234/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/prensa-internacional-informo-no-vacancia-de-ppk-793233/",file=open("open.txt","a"),first=True)
#crawler_url_news("https://diariocorreo.pe/politica/prensa-internacional-informo-no-vacancia-de-ppk-793233/",file=open("open.txt","a"),first=False)
#crawler_url_news("https://diariocorreo.pe/politica/vacancia-ppk-debate-792957/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/roberto-vieira-chile-vacancia-ppk-793225/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/kenji-fujimori-y-hector-becerril-protagonizan-acalorada-discusion-en-el-debate-video-793224/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/san-marcos-y-pucp-se-pronuncian-sobre-debate-vacancia-de-ppk-793222/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/mauricio-mulder-edwin-donayre-vacancia-793221/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/frente-amplio-confirmo-que-votara-favor-de-la-vacancia-de-ppk-793220/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/diputado-chileno-yeni-vilcatoma-condorito-793212/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/correo-las-6-debate-congreso-vacancia-presidencial-793197/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/cecilia-chacon-dicen-no-la-vacancia-porque-ppk-tiene-cara-de-abuelito-793194/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/fiscalia-interrogatorio-keiko-fujimori-28-diciembre-odebrecht-lava-jato-793187/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/kenji-fujimori-anuncia-que-no-apoyara-la-vacancia-presidencial-video-793184/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/mauricio-mulder-el-peru-no-se-derrumbara-si-ppk-es-vacado-el-pais-seguira-adelante-sin-el-video-793176/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/yonhy-lescano-congresistas-accion-popular-vacancia-ppk-pedro-pablo-kuczynski-793172/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/yeni-vilcatoma-comentario-condorito-debate-vacancia-de-ppk-793174/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/oscar-vilchez-critico-lourdes-alcorta-durante-presentacion-de-ppk-793165/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/mercedes-araoz-alberto-fujimori-indulto-793164/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/luz-salgado-alberto-borea-ppk-793161/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/victor-andre-garcia-belaunde-oea-saludo-video-793169/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/garcia-belaunde-comete-fail-citando-garcia-marquez-en-debate-por-vacancia-793159/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/alberto-borea-sobre-ppk-que-eventualmente-uno-se-haya-olvidado-es-causal-para-vacancia-793148/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/miguel-torres-llama-inmoral-ppk-por-culpar-sepulveda-para-salvarse-793155/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ollanta-humala-vacancia-ppk-793154/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/wilbert-rozas-la-presentacion-de-ppk-no-ha-aclarado-nada-793149/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/raul-ferrero-incapacidad-moral-presidente-regulada-793157/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/alberto-borea-este-no-es-un-juicio-politico-es-un-juicio-moral-793131/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppkestoy-aqui-para-dar-la-cara-pues-no-tengo-nada-que-ocultar-793114/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/congresista-edwin-donayre-clinica-ppk-793118/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/exfuncionario-aprista-prision-preventiva-odebrecht-793092/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppk-vacancia-congreso-votos-793096/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/oea-envia-mision-peru-observar-vacancia-legal-793090/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/jorge-nieto-carlos-basombrio-responde-por-actos-793086/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/luz-salgado-critico-mensaje-nacion-pedro-pablo-kuczynski-793072/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/alejandro-toledo-pronuncia-crisis-presidencial-ppk-no-regreso-dictadura-793071/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/daniel-salaverry-vocero-fuerza-popular-caja-preferencial-793070/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/comision-de-transportes-monica-yaya-critica-cambios-en-ley-de-contrataciones-durante-el-nacionalismo-793069/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/justiniano-apaza-denuncia-que-legisladores-fujimoristas-se-ausentan-comision-del-trabaja-793066/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ministro-nieto-confia-en-que-vacancia-presidencial-no-prospere-congresistas-deben-reflexionar-793064/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/toledo-fujimorismo-alista-un-golpe-legislativo-contra-kuczynski-793058/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/osias-ramirez-urge-que-se-trabaje-con-compromiso-y-al-servicio-de-la-comunidad-793057/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppk-presenta-accion-amparo-frenar-su-vacancia-congreso-793038/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/nancy-lange-ppk-corrupcion-video-793030/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/correo-las-6-paolo-guerrero-mundial-rusia-2018-793026/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppk-mercedes-araoz-presidente-793022/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/caso-odebrecht-keiko-fujimori-no-asistio-fiscalia-792977/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/alan-garcia-manda-carta-de-agradecimiento-comision-lava-jato-792962/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppk-carta-oea-observador-crisis-politica-792925/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/armando-villanueva-casos-westfield-first-capital-punta-iceberg-792987/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppk-america-latina-odebrecht-792918/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/jose-hernandez-ppk-aclare-suficiente-informacion-792903/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/gerardo-sepulvera-asegura-que-ppk-no-influyo-en-negocios-de-su-empresa-con-odebrecht-792848/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/ppk-martin-vizcarra-retorno-peru-vacancia-presidencial-792857/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/iglesia-catolica-aldo-mariategui-pico-792757/",file=open("open.txt","a"))
#crawler_url_news("https://diariocorreo.pe/politica/keiko-fujimori-odebrecht-792886/",file=open("open.txt","a"))