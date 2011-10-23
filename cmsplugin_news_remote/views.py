from django.http import HttpResponse
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from cmsplugin_news_remote import utils

def news_detail(request, **kwargs):
    template = "news_detail.html"
    
    plugin = Plugin.objects.get(id = kwargs["plugin_id"])
    news = utils.get_news(plugin.get_cache_path())
    news_object = None
    for news_item in news:
        if kwargs["slug"] == news_item.slug:
            news_object = news_item
            news_item.news_remote_link = reverse(
                'remote_news_detail',
                kwargs={'plugin_id':plugin.id, 'slug':news_item.slug})

    template_data = {
        "object":news_object,
        "latest":news}
    template_context = RequestContext(request, template_data)
    template_filled = loader.get_template(template)
    output = template_filled.render(template_context)
    response = HttpResponse(output, mimetype=None)
    return response

def news_get(request, **kwargs):
    return render_to_response("index.html")