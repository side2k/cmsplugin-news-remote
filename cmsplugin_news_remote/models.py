from django.utils.translation import ugettext_lazy as _
from django.db import models
from cms.models import CMSPlugin
from os.path import join
from django.conf import settings
from cmsplugin_news_remote.utils import update_cache
# Create your models here.
class LatestNewsRemotePlugin(CMSPlugin):
# code is partly borrowed from LatestNewsPlugin model of cmsplugin_news
    """
        Model for the settings when using the latest news cms plugin
    """
    limit = models.PositiveIntegerField(_('Number of news items to show'), 
        help_text=_('Limits the number of items that will be displayed'))
    last_detailed = models.BooleanField(
        _("Show detailed item"), 
        help_text=_("Show detailed version of most recent item"))
# end of borrowed code
    source_url = models.CharField(_('URL of the data source'), 
        max_length=250,
        help_text=_('specifies address for requesting data'))
    
    def get_cache_path(self):
        return join(settings.PROJECT_DIR, "cache/news_remote_%d" % self.id)
        
    def update_cache(self):
        return update_cache(self.get_cache_path(), self.source_url)