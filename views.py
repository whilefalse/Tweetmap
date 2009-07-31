from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
import urllib
import tweetmap.json
from time import time

def home(request):
    f = urllib.urlopen('http://search.twitter.com/trends.json', None,None)
    D = {}
    U = {}
    data = tweetmap.json.read(f.read())
    as_of = data['as_of']
    f.close()
    i=0
    while len(D) != 8:
        d = data['trends'][i]
        url = d['url']
        q = url.split('?')[-1].split('=')[-1]
        i = i +1
        url = 'http://search.twitter.com/search.json?q=%s&since_id=%s' % (q, as_of)
        f = urllib.urlopen(url)
        search_data = tweetmap.json.read(f.read())
        f.close()
        as_of = search_data['max_id']
        D[d['name']] = int(len(search_data['results']))+1
        U[d['name']] = d['url']
    return render_to_response('home.html',{'data':D, 'urls':U}, context_instance=RequestContext(request))
