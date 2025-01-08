# Baca Captcha

import pytesseract

text = pytesseract.image_to_string('hasil.png', , lang="ind")

print(text)