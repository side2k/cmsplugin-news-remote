from django.http import HttpResponse
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from cmsplugin_news_remote import utils

def news_detail(request, **kwargs):
    template = "news_detail.html"
    source = kwargs['source']
    cache_path, source_url = utils.source_params(source)
    news = utils.get_news(cache_path)
    news_object = None
    for news_item in news:
        if kwargs["slug"] == news_item.slug:
            news_object = news_item
            news_item.news_remote_link = reverse(
                'news-remote-details',
                kwargs={'source':source, 'slug':news_item.slug})

    template_data = {
        "object":news_object,
        "latest":news}
    return render_to_response('news_remote/details.html', template_data)


def news_get(request, **kwargs):
    return render_to_response("index.html")