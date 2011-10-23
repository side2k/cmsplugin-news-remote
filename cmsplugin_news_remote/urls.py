from django.conf.urls.defaults import *

from piston.resource import Resource
from news.models import News

from cmsplugin_news_remote.handlers import NewsGetHandler

urlpatterns = patterns('cmsplugin_news_remote.views',
    url(r'^get/(?P<source>[-\w]+)$', Resource(NewsGetHandler), name='news-remote-get'),
    url(r'^details/(?P<source>[-\w]+)/(?P<slug>[-\w]+)/$', 
        'news_detail', name='news-remote-details'),
)

