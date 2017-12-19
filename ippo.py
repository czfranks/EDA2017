
# -*- coding: 850 -*-
#descargar imageMagic
#descargar json,urlib,bs4,PIL si es que no esta instalado obviamente

try: import simplejson as json
except ImportError: import json
from PIL import Image
from urllib import urlopen
from StringIO import StringIO
import urlparse
import urllib
import os
from bs4 import BeautifulSoup


def get_url(manga_number):
	return "http://www.leomanga.com/manga/hajime-no-ippo/capitulo-"+str(manga_number)+"/ssa-scans/es"

def run_crawler(manga_inicial,manga_final): #descargar desde numero de manga(manga_inicial) hasta numero (manga_final)
        ippo_web = "http://www.leomanga.com/"
        for i in range(manga_inicial,manga_final+1):
                error = False
                try:
                        html=urllib.urlopen(get_url(i)).read()
                except:
                        print "ERROR!! in manga : ",i
                        error = True
                if error: continue
                soup = BeautifulSoup(html)
                info = soup.find(id="read-chapter")
                upload = info['name']
                imgs = info['pos'].split(";")
                dir_actual = os.getcwd()+"/"+str(i)
                #print dir_actual
                os.system("mkdir "+str(i));
                dir_actual = dir_actual+"/"
                list_dir_img = []
                for img in imgs:
                        try:
                                data = urlopen(ippo_web+upload+img).read()
                                img_ippo = Image.open(StringIO(data))
                                img_ippo.save(dir_actual+img)
                                list_dir_img.append(dir_actual+img)
                        except:
                                pass

                command = "convert "
                for dir_img in list_dir_img:
                        command=command+"'"+dir_img+"' "
                command=command+"'"+dir_actual+"ippo_"+str(i)+".pdf"+"'"
                os.system(command)

                #os.system("convert *.jpg "+str(i)+".pdf")
                print "Ha descargado -> manga "+str(i)

run_crawler(1115,1152) #descargar desde el manga numero 1115 hasta el 1152

