from funcrunner.actions import *

# passwords.py must exist in the uec-pay directory
from passwords import username, password

set_base_url('http://pay.uec/')
goto('/')

is_link(get_element(text='Log in'))
link_click(get_element(text='Log in'))

url_contains('https://login.staging.launchpad.net/')

get_element(tag='h2', text='Log in to Launchpad Login Service')
is_textfield('id_email')
is_textfield('id_password')
textfield_write('id_email', username)
textfield_write('id_password', password)

button_click(get_element(css_class='btn', name='continue'))

url_contains('https://login.staging.launchpad.net/')
title_is('Authenticate to http://pay.uec/')
button_click(get_element(css_class='btn', name='yes'))


url_is('http://pay.uec/payment/')

get_element(tag='h1', text="Your payment history")
sleep(20)