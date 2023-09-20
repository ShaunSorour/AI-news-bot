import params


def write_html(news_headlines, weather, exchange_rates, spotify):
    try:
        with open("news.html", 'w') as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write("<head>\n")
            file.write("<meta charset='UTF-8'>\n")
            file.write("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'>\n")
            file.write("<style>\n")
            file.write(".category-heading { margin-right: 10px; }\n")
            file.write(".currency-icon { font-size: 16px; margin-left: 5px; }\n")
            # artiist tiles
            file.write(".tile {\n")
            file.write("    display: inline-block;\n")
            file.write("    margin: 10px;\n")
            file.write("    text-align: center;\n")
            file.write("}\n")
            file.write(".tile img {\n")
            file.write("    max-width: 85px;\n")
            file.write("    max-height: 85px;\n")
            file.write("}\n")
            file.write(".icon-text-container {\n")
            file.write("  display: flex;\n")
            file.write("  align-items: center;\n")
            file.write("}\n")
            file.write(".spotify-icon {\n")
            file.write("  font-size: 28px; margin-right: 10px;\n")  # Adjust this value as needed
            file.write("}\n")
            file.write("</style>\n")
            file.write("</head>\n")
            file.write("<body>\n")

            #---------- weather
            file.write("<div style='display: flex;'>\n")
            file.write("<div style='flex: 1; display: flex; align-items: center;'>\n")
            file.write("<ul style='list-style-type: none; display: flex; flex-direction: column; align-items: center;'>\n")
            file.write("<li>\n")
            file.write(f"<img src='{weather['iconURL']}' alt='Weather Icon'>\n")
            file.write("</li>\n")
            file.write("<li>\n")
            file.write(f"<h3>{weather['temp']} °C</h3>\n")
            file.write("</li>\n")
            file.write("</ul>\n")
            file.write("</div>\n")

            #---------- exchange
            file.write("<div style='flex: 1; margin-left: 10px; display: flex; align-items: center;'>\n")
            file.write("<ul style='list-style-type: none;'>\n")
            for currency, rate in exchange_rates.items():
                currency_icon = get_currency_icon_class(currency)
                file.write(f"<li><i class='{currency_icon} currency-icon'></i> {currency}: {rate}</li>\n")
            file.write("</ul>\n")
            file.write("</div>\n")
            file.write("</div>\n")

            #---------- categories
            file.write("<br>\n")
            file.write("<h1>Top Headlines</h1>\n")
            file.write("<ul>\n")
            categories = get_categories(news_headlines)
            for category, items in categories.items():
                if category in params.category_icons:
                    icon_class = params.category_icons[category]
                    file.write(f"<h3><span class='category-heading'>{category.capitalize()}</span><i class='{icon_class}'></i></h3>\n")
                else:
                    file.write(f"<h3>{category.capitalize()}</h3>\n")
                file.write("<ul>\n")
                #------- headlines
                for item in items:
                    headline, link = item
                    file.write(f"<li><a href='{link}' style='text-decoration: none; color: black;'>{headline}</a></li>\n")
                file.write("</ul>\n")
            file.write("</ul>")

            #---------- spotify
            file.write("<br>\n")
            file.write("<br>\n")
            file.write("<div class='icon-text-container'>\n")
            file.write("  <i class='fab fa-spotify spotify-icon'></i>\n")
            file.write("  <h3>Artists to listen to today!</h3>\n")
            file.write("</div>\n")
            for artist in spotify:
                name, image, url = artist.split(" - ")
                file.write("<div class='tile'>\n")
                file.write(f"<h6><a href='{url}' style='text-decoration: none; color: black;' target='_blank'>{name}</a></h6>\n")
                file.write(f"<img src='{image}' alt='{name}'>\n")
                file.write("</div>\n")
            file.write("</body>\n")
            file.write("</html>")
        
        print("HTML created successfully")
        return True
    except Exception as e:
        print("Error writing HTML:", e)


def get_currency_icon_class(currency):
    currency_icons = {
        "USD": "fas fa-dollar-sign",
        "GBP": "fas fa-pound-sign",
        "EUR": "fas fa-euro-sign",
    }
    return currency_icons.get(currency, "fas fa-money-bill-wave")


def get_categories(news_headlines):
    categories = {}
    for headline_data in news_headlines:
        headline, link, category = headline_data
        if category not in categories:
            categories[category] = [] 
        categories[category].append((headline, link))

    return categories