from django.core.management.base import BaseCommand, CommandError
from cms.models import CMSPlugin
from cmsplugin_news_remote.models import LatestNewsRemotePlugin
from cmsplugin_news_remote.utils import update_cache


class Command(BaseCommand):
    help = "Updates cache for remote news plugin"
    
    def handle(self, *args, **options):
        for plugin in LatestNewsRemotePlugin.objects.all():
            print("Updating cache for plugin %d..." % plugin.id)
            print(plugin.update_cache())