import services.email_service as email_service
import services.scraper_service as scraper_service
import services.weather_service as weather_service
import services.bard_service as bard_service
import services.currency_service as currency_service
import services.html_generator as html_generator
import services.spotify as spotify
import params
import asyncio


##################
###### AI ########
AI_Mode = True
##################

if AI_Mode:
    bard_service.get_related_interests()
    bard_service.get_related_news_sources()

news_headlines = scraper_service.scrape_multiple_urls(params.news_sources)
weather = weather_service.weather_details(params.city)
exchange_rates = asyncio.run(currency_service.exchange_rates(params.city))
artists = spotify.get_random_suggested_artist(spotify.get_artist_ID(params.music_artist))
html_generator.write_html(news_headlines, weather, exchange_rates, artists)
email_service.send_email()