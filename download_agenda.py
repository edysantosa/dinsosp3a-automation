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
from babel.dates import format_date
from datetime import date, datetime, timedelta





# https://forums.raspberrypi.com/viewtopic.php?p=2155925#p2155925
# https://stackoverflow.com/questions/53657215/how-to-run-headless-chrome-with-selenium-in-python
# use sudo apt install chromium-chromedriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
service = Service('/usr/bin/chromedriver')
# service = Service('c:\\programdata\\chocolatey\\bin\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Kalau pakai firefox comment yang diatas
# driver = webdriver.Firefox()
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
        cnv.width = ele.width+35; cnv.height = ele.height+30;
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
            time.sleep(2)
            # Simpan gambar capcta
            get_captcha()
            # Olah gambar captcha 
            fix_captcha()
            text = pytesseract.image_to_string('captcha.png', lang="ind")
            print('Captcha : ', text)
            driver.find_element(By.ID, "captcha").send_keys(text)
            
        # click on signin button
        # Hal aneh, kalau pakai chrome pas send keys captcha langsung submit form
        # driver.find_element(By.CLASS_NAME , "btn-wanakerti").click()
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

    if (datetime.now().hour > 12)
        tommorow = date.today() + timedelta(days=1) 
    else
        tommorow = date.today()

    tommorowFormat = format_date(tommorow, "yyyy-MM-dd", locale='id')
    tommorowName = format_date(tommorow, "EEEE, d MMMM yyyy", locale='id')

    def get_request_session(driver):
        import requests
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        return session

    url = "https://kanal.baliprov.go.id/agenda/download_agenda?agenda_date={date}&agenda_type=OPD".format(date=tommorowFormat)
    session = get_request_session(driver)
    r = session.get(url, stream=True)
    chunk_size = 2000
    with open('agenda-{date}.pdf'.format(date=tommorowFormat), 'wb') as file:
        for chunk in r.iter_content(chunk_size):
            file.write(chunk)
except TimeoutException as ex:
    print("TimeoutException has been thrown. " + str(ex))
    driver.quit()

finally:
    # Close the browser session
    driver.quit()
    print('done');

# https://stackoverflow.com/questions/6183276/how-do-i-run-selenium-in-xvfb
