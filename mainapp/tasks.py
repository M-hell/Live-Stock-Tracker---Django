from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.utils import timezone

from mainapp.consumers import STOCKS_GROUP_NAME
from mainapp.services import fetch_nsei_components


@shared_task
def fetch_nsei_components_task() -> str:
    stocks = fetch_nsei_components()
    fetched_at = timezone.now().isoformat()

    channel_layer = get_channel_layer()
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)(
            STOCKS_GROUP_NAME,
            {
                'type': 'stocks.update',
                'stocks': stocks,
                'fetched_at': fetched_at,
            },
        )

    print(f'NSEI components fetched: {len(stocks)}')
    for stock in stocks:
        print(stock)

    return f'fetched {len(stocks)} NSEI components'
