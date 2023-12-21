import streamlit as st 
import validators
import re
import requests
from parsel import Selector
    
def pull_amazon_data(url):
    product_data_list = []

    product_url = url
    try:
        response = requests.get(product_url)
        print(response.status_code)
        if response.status_code == 200:
            sel = Selector(text=response.text)
            variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
            feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]
            price_xpath = '//td[@class="a-color-secondary" and contains(text(), "Price:")]/following-sibling::td/span[contains(@class, "a-price")]/span[@class="a-offscreen"]/text()'

            product_data_list.append({
                "name": sel.css("#productTitle::text").get("").strip(),
                "price": sel.css('.a-price-whole::text').get() + '.' + sel.css('.a-price-fraction::text').get(),
                "price_3": sel.css('.a-offscreen::text').get() ,
                "price_4": sel.css('.a-price-fraction::text').get() ,
                "price_5": sel.css('.a-tex-price::text').get() ,
                "price_2":  sel.xpath(price_xpath).get(),
                "stars": sel.css("i[data-hook=average-star-rating] ::text").get("").strip(),
                "rating_count": sel.css("#acrCustomerReviewText::text").get("").strip(),
                "feature_bullets": feature_bullets,
                "variant_data": variant_data,
            })
    except Exception as e:
            print("Error", e)
        
    return product_data_list

entered_value = st.text_input('Enter SKU or URL', 'test')

if entered_value == 'test':
    st.write('Please input a valid SKU or URL')

if entered_value != 'test' :
    if validators.url(entered_value):
        #It is a URL 
        url = entered_value
    else:
        #It is a SKU
        url = 'https://www.amazon.com/dp/' + entered_value + '/'

    st.write(url)

    result = pull_amazon_data(url=url)
    st.write(result)
