from os import path
from md5 import md5

from django.conf import settings
from django.core.urlresolvers import reverse
from piston.handler import BaseHandler

from cmsplugin_news_remote import utils

class NewsGetHandler(BaseHandler):
    allowed_methods = ("GET",)
    def read(self, request, source=None):
        url = request.GET.get("url","")
        cache_path, source_url = utils.source_params(source)
        utils.check_update_cache(cache_path, source_url)
        news = utils.get_news(cache_path)
        
        def sort_news(item1, item2):
            return cmp(item1.pub_date, item2.pub_date)
            
        news.sort(sort_news, reverse=True)
        data = [{
            'text':news_item.content, 
            'pub_date':news_item.pub_date,
            'is_published':news_item.is_published,
            'url':reverse('news-remote-details', kwargs={'source':source, 'slug':news_item.slug}),
            'title':news_item.title,
            'excerpt':news_item.excerpt} for news_item in news]
        return data