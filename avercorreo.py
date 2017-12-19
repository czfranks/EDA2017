try: import simplejson as json
except ImportError: import json
import urlparse
import urllib
from bs4 import BeautifulSoup


''' *************** COMERCIO ************* '''
#'''
url = "http://elcomercio.pe/tvmas/"
tagPagWeb = "http://elcomercio.pe/tvmas/"
PagWeb = 'Comercio'
#'''
''' *************** CORREO ************* '''
'''
url = 'http://diariocorreo.pe/espectaculos'
tagPagWeb = '/espectaculos/'
PagWeb = 'Correo'
'''
''' *************** PERU21 ************* '''
'''
url = "http://peru21.pe/espectaculos/"
tagPagWeb = "/espectaculos/"
PagWeb = 'Peru21'
'''
'''-------------------------------------------'''
# contador de Noticias
prefixFile = "tvmas/EspectPeru"
idFile = 0
sufixFile = ".json"

urls = [url]
visited = [url]

stopWords = {}
stopWords2 = []

sigPunt = ['.',',',':',';','"','(',')','[',']','-','_']

tildes = []

jsonFecha = ''
jsonTexto = ''
jsonTitulo = ''
jsonTema = ''



def match(tag, url):
    if( len(tag) > len(url) ):
        return False
    for i in range(len(tag)-1):
        if tag[i]!=url[i]:
            return False
    return True

def getMes(mes):
    if(mes=='Enero'):  return '01'
    if(mes=='Febrero'): return '02'
    if(mes=='Marzo'): return '03'
    if(mes=='Abril'): return '04'
    if(mes=='Mayo'): return '05'
    if(mes=='Junio'): return '06'
    if(mes=='Julio'): return '07'
    if(mes=='Agosto'): return '08'
    if(mes=='Setiembre'): return '09'
    if(mes=='Septiembre'): return '09'
    if(mes=='Octubre'): return '10'
    if(mes=='Noviembre'): return '11'
    if(mes=='Diciembre'): return '12'
    return '05'

def getNameFile(c):
    return prefixFile+str(c)+sufixFile

def ShowData(myhtml,count,ListaJson):
    print  "len = " , len(stopWords2)
    try:
        newHtml = urllib.urlopen(myhtml).read()
    except:
        print tagHref
    soup = BeautifulSoup(newHtml)

    print 'TEXTO-----------------------------------------------'
    jsonTexto = ""
    artBody1 = soup.find(itemprop="articleBody")
    if(artBody1):
        for aver in artBody1.find_all('p'):
            if(aver):
                if(not aver.find_all('script')):
                    TextNews1 =  aver.get_text().encode('utf-8')#.decode('unicode-escape')
                    #print TextNews1
                    jsonTexto=jsonTexto+TextNews1
    
    print "KEYWORDS-----------------------------------------------"
    '''artBody = soup.find(itemprop="articleBody")
    if(artBody):
        for aver in artBody.find_all('p'):
            if(aver):
                TextNews =  aver.get_text().encode('utf-8')
                listWordsNews = TextNews.split(" ")
                for word_ in listWordsNews:
                    if stopWords.get(word_.lower()) == None :
                        print normalizar(word_),
                print '\n'
    else:
        return
    '''    
    jsonKeywords = []
    MyKywords = soup.findAll(attrs={"name":"keywords"}) 
    vecKey =  MyKywords[0]['content'].encode('utf-8').split(', ')
    for keycurrent in vecKey:
        #print keycurrent
        jsonKeywords.append(keycurrent) 

    print 'TITULO-----------------------------------------------'
    jsonTitulo =  str(soup.title.string.encode('utf-8')).split(' |')[0]
    print jsonTitulo


    
    print 'FECHA-----------------------------------------------'
    if(PagWeb == "Correo"):
        datePublished = soup.find(itemprop="datePublished")
        if(datePublished):
            fecha = str(datePublished.string.encode('utf-8'))
            LaFecha = fecha.split(' ')
            dia = LaFecha[0]
            mes = LaFecha[2]
            anio = LaFecha[4]
            jsonFecha = str(dia.split()[0]+'/'+getMes(mes).split()[0]+'/'+anio.split()[0])
            #print jsonFecha
            #print soup.find(itemprop="datePublished").string.encode('utf-8')
    if(PagWeb == "Comercio"):
        htmlFecha = soup.findAll(attrs={'class':"fecha"})
        if(htmlFecha):
            htmlFecha0 = htmlFecha[0].get_text()
            hsf = htmlFecha0.split(' ');
            dia = hsf[1].split()[0]
            mes = hsf[3].split()[0]
            anio = hsf[5].split()[0]
            jsonFecha = str(dia)+'/'+str(getMes(mes))+'/'+str(anio)
            #print jsonFecha

    print 'TEMA-----------------------------------------------'
    print "Espectaculos"
    jsonTema = "Espectaculos"

    if(jsonTema == '' or jsonTitulo == '' or jsonTexto == '' or jsonFecha == ''  or jsonKeywords == [] ):
        return 

    ObjNoti = {}
    ObjNoti["Tema"] = jsonTema
    ObjNoti["Titulo"] = jsonTitulo
    ObjNoti["Texto"] = jsonTexto
    ObjNoti["Fecha"] = jsonFecha
    ObjNoti["Keywords"] = jsonKeywords
    ListaJson.append(ObjNoti)

    if(count%10 == 0):
        nameFileJson = getNameFile(count/10)
        with open(nameFileJson, 'a') as outfile:
            json.dump(ListaJson, outfile)
        outfile.close()
        while(len(ListaJson)>1):
            ListaJson.pop()


def runCrawler():
    page_n = '?page='
    counter = 0
    ListaJson = []

    while len(urls)>0:
        try:
            htmltext = urllib.urlopen(urls[0]).read()
        except:
            print urls[0]
        soup = BeautifulSoup(htmltext)

        urls.pop(0)
        
        for tag in soup.findAll('a',href=True):
            if(tag):
                tagHref = tag['href']
                if(not match(tagPagWeb,tagHref)): continue
                tagHref = urlparse.urljoin(url,tagHref)
                if url in tagHref and tagHref not in visited:
                    urls.append(tagHref)
                    visited.append(tagHref)
                    if(page_n in tagHref): continue
                    counter=counter+1
                    print(tagHref)
                    if(tag):
                        ShowData(tagHref,counter,ListaJson)

                    print '-----------------counter = ',counter,'-----------------------------------'
                else:
                    print ""
    print visited
    
runCrawler()

#/espectaculos/cuando-hay-amor-el-sexo-no-averguenza-583984
        
