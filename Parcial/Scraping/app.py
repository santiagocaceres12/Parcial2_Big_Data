import boto3
import csv
import ntpath
from bs4 import BeautifulSoup
import time 

def scraping(path,fname,newspaper,soup,s3,time):
    csvFile = open('/tmp/'+fname+'.csv','w',encoding='utf-8')
    wcsv = csv.writer(csvFile,dialect='unix')
    row = ['title','category','url']
    wcsv.writerow(row)

    if(newspaper == "BBC_News"):
       box = soup.find_all('div',class_='media__content')
       for i in range(len(box)):
         #se busca extraer el titulo el cual se encuentra en un elemento <h3> con la clase 'media__title'.
         if box[i].find('h3',class_='media__title') == None:
            continue
         else:
            title = box[i].find('h3',class_='media__title').get_text()
         #se busca extraer el link el cual se encuentra en un elemento <a> con la clase 'media__link', además de agregar el 'https://www.bbc.com' a los links que les falta. 
         if box[i].find('a',class_='media__link') == None:
            continue
         else:
            if box[i].find('a',class_='media__link').get('href').startswith('https:'):
               link = box[i].find('a',class_='media__link').get('href') 
            else:
               link = 'https://www.bbc.com'+box[i].find('a',class_='media__link').get('href') 
         #se busca extraer la categoria la cual se encuentra en un elemento <a> con la clase 'media__tag tag tag--{}' en los {} se agrega la categoria de la noticia
         if box[i].find('a',class_='media__tag tag tag--news') == None:
            if box[i].find('a',class_='media__tag tag tag--sport') != None:
               category = box[i].find('a',class_='media__tag tag tag--sport').get_text()
            elif box[i].find('a',class_='media__tag tag tag--culture') != None:
               category = box[i].find('a',class_='media__tag tag tag--culture').get_text()
            elif box[i].find('a',class_='media__tag tag tag--future') != None:
               category = box[i].find('a',class_='media__tag tag tag--future').get_text()
            elif box[i].find('a',class_='media__tag tag tag--travel') != None:
               category = box[i].find('a',class_='media__tag tag tag--travel').get_text()
         else:
            category = box[i].find('a',class_='media__tag tag tag--news').get_text()
         row = [title.strip(),category,link]
         wcsv.writerow(row)
    elif(newspaper == "CNN_News"):
       boxCNN = soup.find_all('article',class_='news')
       for i in range(len(boxCNN)):
         titleCNN = boxCNN[i].find('h2',class_='news__title').get_text() #Encuentra la etiqueta h2 con clase news__title y obtiene el texto 
         linkCNN = boxCNN[i].find('a').get('href') #Encuentra la etiqueta a y obtiene el link
         if boxCNN[i].find('span',class_='news__label')==None: #En caso de no encontrar la etiqueta span con clase news__label buscara la etiqueta news__label--photogallery
            if boxCNN[i].find('span',class_='news__label--photogallery')==None:
               continue #En caso de no tenerla continuara
            else:
               categoryCNN = boxCNN[i].find('span',class_='news__label--photogallery').get_text() #En el caso de encontrarla obtendra el texto donde se encontro la clase news__label--photogallery
         else:
            categoryCNN = boxCNN[i].find('span',class_='news__label').get_text() #En el caso de encontrarla obtendra el texto donde se encontro la clase news__label
         rowCNN = [titleCNN.strip(),categoryCNN.strip(),linkCNN]
         wcsv.writerow(rowCNN)
    csvFile.close()
    underFolders = path.replace('headlines/raw','')
    s3.meta.client.upload_file('/tmp/'+fname+'.csv',"resultadosnewscsv",'news/final'+underFolders+'.csv')


def handler(event, context):
    localtime = time.localtime()
    bucketName = event['Records'][0]['s3']['bucket']['name']
    print(bucketName)
    fileName = fileName=event['Records'][0]['s3']['object']['key']
    fileName = fileName.replace('%3D','=')
    s3 = boto3.resource('s3')
    justFileName = ntpath.basename(fileName)
    s3.meta.client.download_file(bucketName, fileName, '/tmp/'+justFileName)
    f = open('/tmp/'+justFileName,'r',encoding='utf-8')
    txt=f.read()
    soup = BeautifulSoup(txt,'html.parser')
    if("BBC_News" in fileName):
        scraping(fileName,justFileName,"BBC_News",soup,s3,localtime)
    elif("CNN_News" in fileName):
        scraping(fileName,justFileName,"CNN_News",soup,s3,localtime)

