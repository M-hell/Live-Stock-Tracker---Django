from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def fetch_nsei_components():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    stocks = []
    try:
        driver.get("https://finance.yahoo.com/quote/%5ENSEI/components/?p=%5ENSEI")
        # Wait until the table tbody is present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table[data-testid="table-container"] tbody tr'))
        )
        rows = driver.find_elements(By.CSS_SELECTOR, 'table[data-testid="table-container"] tbody tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 6:
                stocks.append({
                    'symbol':     cols[0].text.strip(),
                    'company':    cols[1].text.strip(),
                    'last_price': cols[2].text.strip(),
                    'change':     cols[3].text.strip(),
                    'pct_change': cols[4].text.strip(),
                    'volume':     cols[5].text.strip(),
                })
    finally:
        driver.quit()

    return stocks


# Create your views here.
def stockPicker(request):
    stock_picker = fetch_nsei_components()
    print(stock_picker)
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
