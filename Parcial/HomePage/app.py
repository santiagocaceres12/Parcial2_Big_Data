import requests
import boto3
import time

def handler(event, context):
    localtime = time.localtime()
    s3 = boto3.resource('s3')
    get_homepage('https://www.bbc.com/','BBC_News',s3,localtime)
    get_homepage('https://cnnespanol.cnn.com/','CNN_News',s3,localtime)


def get_homepage(url,newspaper,s3,time):
    r = requests.get(url)
    file = "/tmp/homepage"+newspaper+".html"
    f = open(file,'w')
    f.write(r.text)
    f.close()
    data={
	'file':file,
	'bucket':"datahomepage",
	'path':'headlines/raw/newspaper='+newspaper+'/year='+str(time.tm_year)+'/month='+str(time.tm_mon)+'/day='+str(time.tm_mday)+'/homepage.html'
    }
    s3.meta.client.upload_file(data['file'], data['bucket'], data['path'])
