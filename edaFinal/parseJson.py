try: import simplejson as json
except ImportError: import json

import sys
print sys.stdout.encoding

from pprint import pprint

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
	#print len(ans),ans

for i in range(1,2):
	#nameFile = "education.json"
	nameFile = "EspectPeru1.json"
	json_data=open(nameFile).read()

	data = json.loads(json_data)
	
	file = open("bd.txt","w")

	cont=10
	print len(data)
	for arr in data:

		file.write( arr['Tema'].encode('utf-8').strip() )
		file.write("\n")

		Titulo = arr['Titulo'].encode('utf-8').strip()
		file.write(str(len(Titulo)))
		file.write("\n")
		file.write( Titulo )
		file.write("\n")

		texto = arr['Texto'].encode('utf-8').strip()
		arrTexto = texto.split(" ")		
		arrTextoNorm = []
		for w in arrTexto:
			nw = normalize(w)
			if(len(nw) >= 3):
				arrTextoNorm.append(nw)
		file.write(str(len(arrTextoNorm)))
		file.write("\n")
		for w in arrTextoNorm:
			file.write(w)
			file.write(" ")
			print w
		file.write("\n")

		file.write( arr['Fecha'].encode('utf-8').strip() )
		file.write("\n")

		keyWords = arr['Keywords']
		file.write(str(len(keyWords)))
		file.write("\n")
		for key in (keyWords):
			file.write(key.encode('utf-8').strip())
			file.write(" ")
		file.write("\n")
		cont=cont-1
		if(cont==0):
			break
		
	file.close()
		


#for arr in data["array"]:
#	print arr