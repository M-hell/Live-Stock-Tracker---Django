from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer
from mainapp.services import fetch_nsei_components
from django.core.cache import cache


# Create your views here.
def stockPicker(request):
    # stock_picker = fetch_nsei_components()
    # return render(request, 'mainapp/stockpicker.html', {'stockpicker': stock_picker})
    #firsr try to get from cache
    stock_picker = cache.get('stock_picker')
    if stock_picker is not None:
        return render(request, 'mainapp/stockpicker.html', {'stockpicker': stock_picker})
    else:
        #if not in cache, get from service and set to cache
        stock_picker = fetch_nsei_components()
        cache.set('stock_picker', stock_picker, timeout=60*60) #cache for 1 hour
        return render(request, 'mainapp/stockpicker.html', {'stockpicker': stock_picker})

async def asgiui(request):
    return render(request, 'mainapp/asgiui.html')


async def asgitrig(request, trigger_id):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "asgi_group",
        {
            "type": "asgi.trigger",
            "id": trigger_id,
        },
    )
    return HttpResponse(f"Triggered id: {trigger_id}")
