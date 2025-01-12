# Kirim pesan ke whatsapp server
import requests
import base64
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mengirim pesan ke whatsapp"
    )

    parser.add_argument("--phone", default="081999066412", help="Nomor whatsapp")
    parser.add_argument("--message", default="Heehheheheh", help="Pesan yang dikirim")
    args = parser.parse_args()
    phone = args.number
    message = args.message

    headers = {"Content-Type": "application/json;charset=utf-8"}
    json_payload = {
        "phone_number": number,
        "caption": message
    }
    url = 'http://localhost:8000/send-message'
    r = requests.post(url, headers=headers, json=json_payload)
    print (r.json())
