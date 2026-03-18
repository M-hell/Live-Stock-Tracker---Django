from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer
from mainapp.services import fetch_nsei_components


# Create your views here.
def stockPicker(request):
    stock_picker = fetch_nsei_components()
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
