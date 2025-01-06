# Kirim pesan ke whatsapp server
import requests
import base64

# Kirim agenda ke server whatsapp
# headers = {"Content-Type": "application/json;charset=utf-8"}
# json_payload = {
#     "phone_number": "081999066412",
#     "message": "Heheheheheheheh he"
# }
# url = 'http://localhost:8000/send-message'
# r = requests.post(url, headers=headers, json=json_payload)
# print (r.json())

with open("agenda-2025-01-03.pdf", "rb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())
headers = {"Content-Type": "application/json;charset=utf-8"}
json_payload = {
    "phone_number": "081999066412",
    "caption": "Agenda Kapan-kapan",
    "mimetype": "application/pdf",
    "filename": "agenda-2025-01-03.pdf",
    "file": encoded_string.decode("utf-8")
}
url = 'http://localhost:8000/send-file'
r = requests.post(url, headers=headers, json=json_payload)
print (r.json())
