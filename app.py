from pyotp import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import cv2
import numpy as np
from PIL import Image, ImageDraw
import pytesseract
import time

driver = webdriver.Firefox()
driver.get("https://sso.baliprov.go.id/")
wait = WebDriverWait(driver, 5)
driver.maximize_window()


def fix_captcha():
    img = cv2.imread("captcha.jpg")

    # invert warna
    img = cv2.bitwise_not(img)

    # dilate image
    kernel = np.ones((2,2),np.uint8)
    dilation = cv2.dilate(img,kernel,iterations = 1)
    # erode image
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    # clean 
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    hasil = cv2.bitwise_not(opening)
    cv2.imwrite('./captcha.png', hasil)

    # cv2.imshow('image',hasil)
    # cv2.waitKey(0)

def get_captcha():
    # find the captcha element
    ele_captcha = driver.find_element("id", "captcha-img")

    # get the captcha as a base64 string
    import base64
    img_base64 = driver.execute_script("""
        var ele = arguments[0];
        var cnv = document.createElement('canvas');
        cnv.width = ele.width+15; cnv.height = ele.height+15;
        cnv.getContext('2d').drawImage(ele, 0, 0);
        return cnv.toDataURL('image/jpeg').substring(22);    
        """, ele_captcha)
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_base64))

try:
    authRadio = 0
    while not authRadio:
        # enter the email and password
        email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        email.send_keys("edy.santosa.p@gmail.com")
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys("Bali2020!@#")

        # OCR captcha
        text = ''
        while not text.strip():
            driver.find_element(By.CLASS_NAME , "btn-chg-captcha").click()
            time.sleep(1)
            # Simpan gambar capcta
            get_captcha()
            # Olah gambar captcha 
            fix_captcha()
            text = pytesseract.image_to_string('captcha.png')
            print('Captcha : ', text)
            driver.find_element(By.ID, "captcha").send_keys(text)
            
        # click on signin button
        driver.find_element(By.CLASS_NAME , "btn-wanakerti").click()
        try:       
            authRadio = wait.until(EC.presence_of_element_located((By.ID, "customRadio2")))
            # select login with authenticator code
            driver.find_element(By.XPATH , '/html/body/div[3]/div[2]/div/form/div[2]/div[2]/div[2]/label').click()
            driver.find_element(By.CLASS_NAME , "btn-primary").click()
            #wait for the 2FA feild to display
            authField = wait.until(EC.presence_of_element_located((By.NAME, "one_time_password")))
            # get the token from google authenticator
            totp = TOTP("A3EADTZRIRS3B3Z6")
            token = totp.now()
            # enter the token in the UI
            authField.send_keys(token)
            # click on the button to complete 2FA
            driver.find_element(By.ID , "btn-sign-in").click()
        except TimeoutException as ex: 
            print("TimeoutException has been thrown. " + str(ex))
            driver.find_element(By.CLASS_NAME , "confirm").click()
            continue

    # Download agenda
    time.sleep(2)
    driver.get("https://kanal.baliprov.go.id/internal")
    time.sleep(2)
    driver.get("https://kanal.baliprov.go.id/agenda/download_agenda?agenda_date=2025-01-06&agenda_type=OPD")

except TimeoutException as ex:
    print("TimeoutException has been thrown. " + str(ex))
    driver.quit()

finally:
    # Close the browser session
    #driver.quit()
    print('done');

# https://stackoverflow.com/questions/5370762/how-to-hide-firefox-window-selenium-webdriver/23898148#23898148
