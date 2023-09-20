from secret import currency_base_url
import requests
import asyncio


def get_exchange_rate(base_currency, currency):
    try:
        url = f"{currency_base_url}{currency}/{base_currency}.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            response = response.json()
            rate = response[base_currency]
            return rate
        else:
            return None
    except Exception as e:
        print("Error getting exchange rates:", e)


async def exchange_rates(city):
    # want to use city to set currency
    # either bard or country api
    if "cape town" in city.lower():
        base_currency = "zar"

    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(None, get_exchange_rate, base_currency, "usd"),
        loop.run_in_executor(None, get_exchange_rate, base_currency, "gbp"),
        loop.run_in_executor(None, get_exchange_rate, base_currency, "eur")
    ]
    usd, gbp, eur = await asyncio.gather(*tasks)

    usd = round(usd, 2)
    gbp = round(gbp, 2)
    eur = round(eur, 2)

    currency = {
        "USD": usd,
        "GBP": gbp,
        "EUR": eur
    }
    print("Exhange rates successfully retrieved")

    return currency