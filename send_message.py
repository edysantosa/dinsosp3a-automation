# Kirim pesan ke whatsapp server
import requests
import base64
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mengirim pesan ke whatsapp"
    )

    parser.add_argument("--groupname", required=True, help="Nama grup whatsapp")
    parser.add_argument("--message", required=True, help="Pesan yang dikirim")
    args = parser.parse_args()

    groupName = args.groupname
    message = args.message

    headers = {"Content-Type": "application/json;charset=utf-8"}
    json_payload = {
        "group_name": groupName,
        "message": message
    }
    url = 'http://localhost:8000/send-group-message'
    r = requests.post(url, headers=headers, json=json_payload)
    print (r.json())
