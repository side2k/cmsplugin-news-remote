from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from news.models import News

from cmsplugin_news_remote.models import LatestNewsRemotePlugin
from cmsplugin_news_remote import utils

from django.core import serializers
from django.core.urlresolvers import reverse
from django.conf import settings

from datetime import datetime
import urllib2
import socket
import os

cache_expire_time = 5*60 #in seconds

class CMSNewsRemotePlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = LatestNewsRemotePlugin
    name = _('Remote latest news')
    render_template = "news_remote_latest.html"
    

    def render(self, context, instance, placeholder):
        """
            Render the latest news
        """
        news = utils.get_news(instance.get_cache_path())
        if instance.last_detailed:
            obj = news[0]
            self.render_template = "news_remote_detailed.html"
            context.update({"object":obj})
        else:
            latest = news[:instance.limit]
            for news_item in latest:
                news_item.news_remote_link = reverse(
                    "remote_news_detail", kwargs={"plugin_id":instance.id, "slug":news_item.slug})
            context.update({
                'instance': instance,
                'latest': latest,
                'placeholder': placeholder,
            })
        return context

plugin_pool.register_plugin(CMSNewsRemotePlugin)