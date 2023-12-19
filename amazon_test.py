
def pull_amazon_data(url):

    import re
    import requests
    from parsel import Selector
    
    product_data_list = []

    product_url = url
    try:
        response = requests.get(product_url)
        print(response.status_code)
        if response.status_code == 200:
            sel = Selector(text=response.text)
            variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
            feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]
            print('here1')
            product_data_list.append({
                "name": sel.css("#productTitle::text").get("").strip(),
                "price": sel.css('.a-price-whole::text').get() + '.' + sel.css('.a-price-fraction::text').get(),
                "price_2": sel.css('div.a-spacing-small span.a-price-whole:text').get(),
                "stars": sel.css("i[data-hook=average-star-rating] ::text").get("").strip(),
                "rating_count": sel.css("#acrCustomerReviewText::text").get("").strip(),
                #"feature_bullets": feature_bullets,
                #"variant_data": variant_data,
            })
    except Exception as e:
            print("Error", e)
        
    return product_data_list