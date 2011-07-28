from django.http import HttpResponse
from django.template import loader, RequestContext
from cmsplugin_news_remote import utils
from cmsplugin_news_remote.models import LatestNewsRemotePlugin as Plugin

def news_detail(request, **kwargs):
    template = "news_detail.html"
    
    plugin = Plugin.objects.get(id = kwargs["plugin_id"])
    news = utils.get_news(plugin.get_cache_path())
    news_object = None
    for news_item in news:
        if kwargs["slug"] == news_item.slug:
            news_object = news_item
            break
    template_data = {
        "object":news_object}
    template_context = RequestContext(request, template_data)
    template_filled = loader.get_template(template)
    output = template_filled.render(template_context)
    response = HttpResponse(output, mimetype=None)
    return response
