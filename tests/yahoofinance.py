from funcrunner.actions import *

goto('http://finance.search.yahoo.com/')
title_contains('Yahoo!')
element = get_element(id='yschsp')
textfield_write(element, 'IBM')
element = get_element(id='yschbt')
button_click(element)
title_contains('IBM')
    