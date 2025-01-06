# save gambar capcha cara 2

import base64
from selenium import webdriver

driver = webdriver.Firefox()
driver.set_script_timeout(10)

driver.get("http://sso.baliprov.go.id")
driver.maximize_window()

# find the captcha element
ele_captcha = driver.find_element("id", "captcha-img")

# get the captcha as a base64 string
import base64
img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height+5;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, ele_captcha)
with open(r"image.jpg", 'wb') as f:
    f.write(base64.b64decode(img_base64))