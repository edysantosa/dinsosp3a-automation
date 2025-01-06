# save gambar capcha

from PIL import Image, ImageDraw
from selenium import webdriver

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    image = image.crop((left, top, right, bottom))  # defines crop points

    # draw = ImageDraw.Draw(image)
    # draw.rectangle(((location['x'], location['y']), (location['x'] + size['width'], location['y'] + size['height'])), fill="black")

    image.save(path, 'png')  # saves new cropped image


driver = webdriver.Firefox()
driver.get("http://sso.baliprov.go.id")

# download image/captcha
img = driver.find_element("id", "captcha-img")
get_captcha(driver, img, "captcha.png")
driver.quit()