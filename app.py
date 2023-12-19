from amazon_test import pull_amazon_data
import streamlit as st 
import validators

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
