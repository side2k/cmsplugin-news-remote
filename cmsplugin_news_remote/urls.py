from django.conf.urls.defaults import *

from news.models import News

news_info_dict = {
    'news':[1,2,3]
}

news_info_month_dict = {
    #'queryset': News.published.all(),
    'queryset': [1,2,3],
    'date_field': 'pub_date',
    'month_format': '%m',
}

urlpatterns = patterns('cmsplugin_news_remote.views',
    url(r'^get/$', 'news_get', name='news-remote-get'),
    (r'^(?P<plugin_id>\d+)/(?P<slug>[-\w]+)/$', 
        'news_detail', news_info_dict, 'remote_news_detail'),
)

