import os
from os import path
import urllib2
import socket
from md5 import md5
from datetime import datetime

from django.core import serializers
from django.conf import settings



def update_cache(path, source_url):
    prev_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(2)
        url = urllib2.urlopen(source_url)
        data = url.read()
        url.close()        
    except Exception, raised_exception:
        status = "couldn't read from url: %s" % raised_exception
        return status
        return False
    finally:
        socket.setdefaulttimeout(prev_timeout)
    status = "read %d bytes from url" % len(data)
    cache_file = open(path, "w")
    try:
        cache_file.write(data)
    finally:
        cache_file.close()
    return status
    
def check_update_cache(path, source_url):
    #check last cache modification
    cache_expired = True
    try:
        cache_stats = os.stats(cache_file)
        cache_mtime = datetime.fromtimestamp(cache_stats.st_mtime)
        delta = cache_mtime - datetime.now()
        delta_seconds = delta.days * 86400 + delta.seconds
        cache_expired = delta_seconds >= cache_expire_time
    except:
        pass #cache needs to be recreated
    
    if cache_expired:
        status = update_cache(path, source_url)
    return status
    
    
def get_news(cache_file_path=None):
    data_file = open(cache_file_path, "r")    
    
    try:
        data_json = data_file.read()
    finally:
        data_file.close()
    #news_debug = News()
    #news_debug.title = status
    #latest = [news_debug] #News.published.all()[:instance.limit]        
    data = serializers.deserialize("json", data_json)
    news = []
    for news_item in data:
        if news_item.object.is_published:
            if news_item.object.unpub_date != None:
                if news_item.object.unpub_date < datetime.now():
                    continue
            news += [news_item.object]
    return news
    
def source_params(source):
    source_url = settings.NEWS_SOURCES[source]
    cache_filename = 'news_%s' % md5(source_url).hexdigest()
    cache_path = path.join(settings.PROJECT_DIR, 'cache', cache_filename)
    return (cache_path, source_url)